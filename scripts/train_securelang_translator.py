# scripts/train_securelang_translator.py
import argparse
import json
from pathlib import Path


def load_pairs(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            rows.append(
                {
                    "source": f"Translate C to SecureLang preserving CWE behavior ({item['cwe']}):\n{item['source_c']}",
                    "target": item["target_securelang"],
                }
            )
    return rows


def tokenize_function(examples, tokenizer, max_source_len, max_target_len):
    model_inputs = tokenizer(
        examples["source"],
        max_length=max_source_len,
        truncation=True,
    )
    labels = tokenizer(
        text_target=examples["target"],
        max_length=max_target_len,
        truncation=True,
    )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


def is_codebert_model(model_name: str) -> bool:
    lowered = model_name.lower()
    return "codebert" in lowered


def build_model_and_tokenizer(model_name: str):
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, EncoderDecoderModel

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if is_codebert_model(model_name):
        model = EncoderDecoderModel.from_encoder_decoder_pretrained(model_name, model_name)
        pad_id = tokenizer.pad_token_id
        if pad_id is None:
            tokenizer.add_special_tokens({"pad_token": "<pad>"})
            pad_id = tokenizer.pad_token_id
            model.encoder.resize_token_embeddings(len(tokenizer))
            model.decoder.resize_token_embeddings(len(tokenizer))
        start_id = tokenizer.cls_token_id if tokenizer.cls_token_id is not None else tokenizer.bos_token_id
        end_id = tokenizer.sep_token_id if tokenizer.sep_token_id is not None else tokenizer.eos_token_id
        if start_id is None or end_id is None:
            raise ValueError("CodeBERT model requires cls/sep or bos/eos tokens")
        model.config.decoder_start_token_id = start_id
        model.config.eos_token_id = end_id
        model.config.pad_token_id = pad_id
        model.config.vocab_size = model.config.decoder.vocab_size
        return model, tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return model, tokenizer


def run(args):
    rows = load_pairs(Path(args.dataset))
    if not rows:
        raise ValueError("No rows available in translation dataset")

    from datasets import Dataset
    from transformers import DataCollatorForSeq2Seq, Trainer, TrainingArguments

    dataset = Dataset.from_list(rows)
    split = dataset.train_test_split(test_size=args.eval_ratio, seed=args.seed)

    model, tokenizer = build_model_and_tokenizer(args.model)

    tokenized_train = split["train"].map(
        tokenize_function,
        batched=True,
        fn_kwargs={
            "tokenizer": tokenizer,
            "max_source_len": args.max_source_len,
            "max_target_len": args.max_target_len,
        },
        remove_columns=split["train"].column_names,
    )
    tokenized_eval = split["test"].map(
        tokenize_function,
        batched=True,
        fn_kwargs={
            "tokenizer": tokenizer,
            "max_source_len": args.max_source_len,
            "max_target_len": args.max_target_len,
        },
        remove_columns=split["test"].column_names,
    )

    collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        num_train_epochs=args.epochs,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_steps=20,
        report_to=[],
        fp16=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        tokenizer=tokenizer,
        data_collator=collator,
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    print(f"Training complete. Model saved to {args.output_dir}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="datasets/llm_translation_dataset.jsonl")
    parser.add_argument("--model", default="google/flan-t5-base")
    parser.add_argument("--output-dir", default="models/securelang-translator")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--eval-ratio", type=float, default=0.1)
    parser.add_argument("--max-source-len", type=int, default=512)
    parser.add_argument("--max-target-len", type=int, default=256)
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
