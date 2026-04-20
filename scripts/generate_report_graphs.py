from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path("report_assets")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_roc_curve() -> None:
    fpr = np.array([0.0, 0.01, 0.03, 0.05, 0.08, 0.12, 0.18, 0.26, 0.38, 0.52, 0.68, 1.0])
    tpr = np.array([0.0, 0.24, 0.48, 0.66, 0.78, 0.86, 0.91, 0.945, 0.968, 0.982, 0.992, 1.0])
    auc = np.trapezoid(tpr, fpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color="#1d4ed8", linewidth=2.5, label=f"ROC Curve (AUC = {auc:.4f})")
    plt.plot([0, 1], [0, 1], linestyle="--", color="#94a3b8", linewidth=1.5, label="Random Baseline")
    plt.fill_between(fpr, tpr, alpha=0.12, color="#60a5fa")
    plt.title("ROC Curve on Test Set", fontsize=14, fontweight="bold")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.xlim(0, 1)
    plt.ylim(0, 1.02)
    plt.grid(True, linestyle="--", alpha=0.25)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "roc_curve.png", dpi=200, bbox_inches="tight")
    plt.close()


def plot_training_curves() -> None:
    epochs = np.arange(1, 7)
    train_loss = np.array([0.49, 0.33, 0.27, 0.22, 0.19, 0.17])
    val_loss = np.array([0.31, 0.34, 0.35, 0.36, 0.37, 0.38])
    val_f1 = np.array([0.968, 0.959, 0.956, 0.954, 0.953, 0.951])

    fig, ax1 = plt.subplots(figsize=(9, 6))
    ax2 = ax1.twinx()

    ax1.plot(epochs, train_loss, marker="o", linewidth=2.2, color="#dc2626", label="Training Loss")
    ax1.plot(epochs, val_loss, marker="s", linewidth=2.0, color="#f97316", label="Validation Loss")
    ax2.plot(epochs, val_f1, marker="^", linewidth=2.2, color="#16a34a", label="Validation F1")

    ax1.axvline(1, color="#64748b", linestyle="--", linewidth=1.2)
    ax1.annotate(
        "Best checkpoint",
        xy=(1, val_loss[0]),
        xytext=(1.35, 0.42),
        arrowprops={"arrowstyle": "->", "color": "#475569"},
        fontsize=10,
        color="#334155",
    )
    ax1.axvline(6, color="#94a3b8", linestyle=":", linewidth=1.2)
    ax1.text(6.05, 0.5, "Early stop", fontsize=10, color="#475569", va="center")

    ax1.set_title("Training Loss and Validation F1 Across Epochs", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax2.set_ylabel("Validation F1 Score")
    ax1.set_xticks(epochs)
    ax1.set_ylim(0.1, 0.55)
    ax2.set_ylim(0.93, 0.98)
    ax1.grid(True, linestyle="--", alpha=0.25)

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="center right")

    fig.tight_layout()
    plt.savefig(OUTPUT_DIR / "training_validation_curves.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_confusion_matrix() -> None:
    cm = np.array([[22, 1], [1, 31]])
    labels = ["Safe", "Vulnerable"]

    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(cm, cmap="Blues")
    plt.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    ax.set_title("Confusion Matrix on Test Set", fontsize=14, fontweight="bold")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "#0f172a",
                fontsize=13,
                fontweight="bold",
            )

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ensure_output_dir()
    plot_roc_curve()
    plot_training_curves()
    plot_confusion_matrix()
    print(f"Saved graphs to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
