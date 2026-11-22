
import os
import sys
import time
import subprocess
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPO_DIR = os.path.join(BASE_DIR, "Real-ESRGAN")
SCRIPT_PATH = os.path.join(REPO_DIR, "inference_realesrgan.py")

INPUT_DIR = os.path.join(BASE_DIR, "data", "degraded", "contrast")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "restored", "contrast")

REPORT_DIR = os.path.join(BASE_DIR, "reports")
TIME_CSV = os.path.join(REPORT_DIR, "contrast_restoration_times.csv")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    images = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    print(f"Images to restore: {len(images)}")

    results = []

    for index, filename in enumerate(images, start=1):

        input_path = os.path.join(INPUT_DIR, filename)

        command = [
            sys.executable,
            SCRIPT_PATH,
            "-n", "RealESRGAN_x4plus",
            "-i", input_path,
            "-o", OUTPUT_DIR,
            "--fp32",
            "-t", "256"
        ]

        print(f"\n[{index}/{len(images)}] Restoring: {filename}")

        start = time.time()

        try:
            subprocess.run(command, cwd=REPO_DIR, check=True)
            elapsed = time.time() - start

            results.append([filename, round(elapsed, 2), "Success"])

            print(f"Completed in {elapsed:.2f} seconds")

        except subprocess.CalledProcessError as error:
            results.append([filename, "", "Failed"])
            print(f"Restoration failed: {error}")

    with open(TIME_CSV, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "filename",
            "processing_time_seconds",
            "status"
        ])

        writer.writerows(results)

    successful = sum(1 for row in results if row[2] == "Success")

    print("\nBATCH RESTORATION FINISHED")
    print(f"Successful: {successful}/{len(images)}")
    print(f"Time report: {TIME_CSV}")


if __name__ == "__main__":
    main()
