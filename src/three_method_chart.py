
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "reports")

CSV_PATH = os.path.join(REPORT_DIR, "final_comparison.csv")

# Load comparison data
df = pd.read_csv(CSV_PATH)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

required_columns = [
    "category",
    "degraded_psnr",
    "opencv_psnr",
    "restored_psnr",
    "degraded_ssim",
    "opencv_ssim",
    "restored_ssim"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing CSV columns: {missing}")

# Calculate average metrics for each category
averages = df.groupby("category", as_index=False)[
    required_columns[1:]
].mean()

categories = averages["category"].tolist()
x = np.arange(len(categories))
width = 0.25

os.makedirs(REPORT_DIR, exist_ok=True)


def create_chart(metric, ylabel, title, filename):
    fig, ax = plt.subplots(figsize=(11, 6))

    methods = [
        ("degraded_" + metric, "Degraded"),
        ("opencv_" + metric, "OpenCV"),
        ("restored_" + metric, "Real-ESRGAN")
    ]

    for i, (column, label) in enumerate(methods):
        bars = ax.bar(
            x + (i - 1) * width,
            averages[column],
            width,
            label=label
        )

        ax.bar_label(bars, fmt="%.3f", padding=3, fontsize=8)

    ax.set_xlabel("Degradation Category")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()

    output_path = os.path.join(REPORT_DIR, filename)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    print(f"Chart saved: {output_path}")


# Generate PSNR chart
create_chart(
    metric="psnr",
    ylabel="PSNR (dB)",
    title="PSNR Comparison: Three Restoration Methods",
    filename="average_psnr_comparison.png"
)

# Generate SSIM chart
create_chart(
    metric="ssim",
    ylabel="SSIM",
    title="SSIM Comparison: Three Restoration Methods",
    filename="average_ssim_comparison.png"
)

# Save average values for reporting
averages.to_csv(
    os.path.join(REPORT_DIR, "average_comparison_metrics.csv"),
    index=False
)

print("\nComparison charts generated successfully.")
