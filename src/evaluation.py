
import os
import cv2
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

# Project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORIGINAL_DIR = os.path.join(BASE_DIR, "data", "original")
DEGRADED_DIR = os.path.join(BASE_DIR, "data", "degraded")
RESTORED_DIR = os.path.join(BASE_DIR, "outputs", "restored")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

CATEGORIES = ["blur", "noise", "low_resolution", "contrast"]


def calculate_metrics(reference, test_image):
    """Calculate PSNR and SSIM between two images."""

    psnr = peak_signal_noise_ratio(
        reference,
        test_image,
        data_range=255
    )

    ssim = structural_similarity(
        reference,
        test_image,
        channel_axis=2,
        data_range=255
    )

    return psnr, ssim


def evaluate_image(filename, category):
    """Compare degraded and restored images with the clean original."""

    original_path = os.path.join(ORIGINAL_DIR, filename)
    degraded_path = os.path.join(DEGRADED_DIR, category, filename)

    name, extension = os.path.splitext(filename)
    restored_filename = name + "_out" + extension
    restored_path = os.path.join(RESTORED_DIR, category, restored_filename)
    # Read images
    original = cv2.imread(original_path)
    degraded = cv2.imread(degraded_path)
    restored = cv2.imread(restored_path)

    if original is None or degraded is None or restored is None:
        print(f"Skipping {category}/{filename}: Image not found.")
        return None

    # Ensure degraded image matches reference dimensions
    degraded = cv2.resize(
        degraded,
        (original.shape[1], original.shape[0])
    )

    # Resize restored image to reference dimensions
    restored = cv2.resize(
        restored,
        (original.shape[1], original.shape[0]),
        interpolation=cv2.INTER_AREA
    )

    # Calculate metrics
    degraded_psnr, degraded_ssim = calculate_metrics(
        original, degraded
    )

    restored_psnr, restored_ssim = calculate_metrics(
        original, restored
    )

    print(f"\nCategory: {category}")
    print(f"Degraded PSNR: {degraded_psnr:.4f} dB")
    print(f"Degraded SSIM: {degraded_ssim:.4f}")
    print(f"Restored PSNR: {restored_psnr:.4f} dB")
    print(f"Restored SSIM: {restored_ssim:.4f}")

    return {
        "image": filename,
        "category": category,
        "degraded_psnr": degraded_psnr,
        "degraded_ssim": degraded_ssim,
        "restored_psnr": restored_psnr,
        "restored_ssim": restored_ssim
    }


def main():
    os.makedirs(REPORT_DIR, exist_ok=True)

    results = []

    image_files = [
        filename for filename in os.listdir(ORIGINAL_DIR)
        if filename.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not image_files:
        print("No original images found.")
        return

    for filename in image_files:
        for category in CATEGORIES:
            result = evaluate_image(filename, category)

            if result is not None:
                results.append(result)

    if results:
        dataframe = pd.DataFrame(results)

        report_path = os.path.join(
            REPORT_DIR,
            "quality_metrics.csv"
        )

        dataframe.to_csv(report_path, index=False)

        print("\nEvaluation completed.")
        print(f"Results saved to: {report_path}")
    else:
        print("No images were evaluated.")


if __name__ == "__main__":
    main()
