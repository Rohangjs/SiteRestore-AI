
import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPO_DIR = os.path.join(BASE_DIR, "Real-ESRGAN")
SCRIPT_PATH = os.path.join(REPO_DIR, "inference_realesrgan.py")

INPUT_DIR = os.path.join(BASE_DIR, "data", "degraded")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "restored")

CATEGORIES = ["blur", "noise", "low_resolution", "contrast"]


def restore_image(category, filename):

    input_path = os.path.join(INPUT_DIR, category, filename)
    output_folder = os.path.join(OUTPUT_DIR, category)

    os.makedirs(output_folder, exist_ok=True)

    command = [
        sys.executable,
        SCRIPT_PATH,
        "-n", "RealESRGAN_x4plus",
        "-i", input_path,
        "-o", output_folder,
        "--fp32",
        "-t", "256"
    ]

    print(f"\nRestoring: {category}/{filename}")

    start_time = time.time()

    subprocess.run(command, cwd=REPO_DIR, check=True)

    elapsed_time = time.time() - start_time

    print(f"Completed: {category}/{filename}")
    print(f"Processing time: {elapsed_time:.2f} seconds")

    return elapsed_time


def main():

    total_start = time.time()

    for category in CATEGORIES:

        category_folder = os.path.join(INPUT_DIR, category)

        for filename in os.listdir(category_folder):

            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                restore_image(category, filename)

    total_time = time.time() - total_start

    print("\nAll images restored successfully.")
    print(f"Total processing time: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()
