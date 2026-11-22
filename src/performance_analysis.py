
import os
import csv
import statistics
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "reports")

CATEGORIES = [
    "blur",
    "noise",
    "low_resolution",
    "contrast"
]

summary = []

for category in CATEGORIES:
    csv_path = os.path.join(
        REPORT_DIR,
        f"{category}_restoration_times.csv"
    )

    times = []

    with open(csv_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["status"] == "Success":
                times.append(float(row["processing_time_seconds"]))

    if times:
        summary.append({
            "category": category,
            "images_processed": len(times),
            "total_time_seconds": round(sum(times), 2),
            "average_time_seconds": round(statistics.mean(times), 2),
            "median_time_seconds": round(statistics.median(times), 2)
        })

output_csv = os.path.join(REPORT_DIR, "performance_summary.csv")

with open(output_csv, "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "category",
            "images_processed",
            "total_time_seconds",
            "average_time_seconds",
            "median_time_seconds"
        ]
    )
    writer.writeheader()
    writer.writerows(summary)

categories = [item["category"] for item in summary]
averages = [item["average_time_seconds"] for item in summary]

plt.figure(figsize=(10, 6))
bars = plt.bar(categories, averages)

plt.title("Average Real-ESRGAN Processing Time")
plt.xlabel("Degradation Category")
plt.ylabel("Average Processing Time (seconds)")
plt.grid(axis="y", linestyle="--", alpha=0.5)

for bar, value in zip(bars, averages):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.2f}s",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

chart_path = os.path.join(
    REPORT_DIR,
    "processing_time_comparison.png"
)

plt.savefig(chart_path, dpi=300)
plt.close()

print("PERFORMANCE ANALYSIS COMPLETED")
print(f"Summary CSV: {output_csv}")
print(f"Chart: {chart_path}")

for item in summary:
    print(
        f'{item["category"]}: '
        f'{item["average_time_seconds"]} seconds/image'
    )
