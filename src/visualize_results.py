
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_PATH = os.path.join(BASE_DIR, "reports", "quality_metrics.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "reports")

df = pd.read_csv(CSV_PATH)

metrics = [
    ("degraded_psnr", "restored_psnr", "PSNR (dB)"),
    ("degraded_ssim", "restored_ssim", "SSIM")
]

for degraded_col, restored_col, metric_name in metrics:

    categories = df["category"]
    x = range(len(categories))
    width = 0.35

    plt.figure(figsize=(10, 5))

    plt.bar(
        [i - width / 2 for i in x],
        df[degraded_col],
        width,
        label="Before Restoration"
    )

    plt.bar(
        [i + width / 2 for i in x],
        df[restored_col],
        width,
        label="After Restoration"
    )

    plt.xticks(list(x), categories)
    plt.ylabel(metric_name)
    plt.title(f"Real-ESRGAN Restoration: {metric_name} Comparison")
    plt.legend()
    plt.tight_layout()

    filename = metric_name.lower().replace(" ", "_") + "_comparison.png"
    output_path = os.path.join(OUTPUT_DIR, filename)

    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved: {output_path}")

print("\nComparison charts generated successfully.")
