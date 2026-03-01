import torch
from pipeline.compiler_pipeline import SecureCompilerPipeline
from models.fusion_model import SecureFusionModel


def analyze_code(code, model):

    pipeline = SecureCompilerPipeline()

    graph, errors = pipeline.compile_to_pdg(code)

    if errors:
        print("Compilation Errors:")
        for e in errors:
            print(e)
        return

    model.eval()
    with torch.no_grad():
        output = model(code, graph)
        prediction = torch.argmax(output, dim=1).item()

    if prediction == 1:
        print("⚠️ Vulnerability Detected")
    else:
        print("✅ Code is Safe")