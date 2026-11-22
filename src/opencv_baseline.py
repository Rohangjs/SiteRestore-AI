
import os
import cv2
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

# Project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORIGINAL_DIR = os.path.join(BASE_DIR, "data", "original")
DEGRADED_DIR = os.path.join(BASE_DIR, "data", "degraded")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "opencv_baseline")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

CATEGORIES = ["blur", "noise", "low_resolution", "contrast"]


# 1. Unsharp masking for blurred images
def enhance_blur(image):
    blurred = cv2.GaussianBlur(image, (0, 0), 2)
    return cv2.addWeighted(image, 1.8, blurred, -0.8, 0)


# 2. Non-local means denoising
def remove_noise(image):
    return cv2.fastNlMeansDenoisingColored(
        image,
        None,
        h=10,
        hColor=10,
        templateWindowSize=7,
        searchWindowSize=21
    )


# 3. Mild sharpening for low-resolution images
def enhance_low_resolution(image):
    blurred = cv2.GaussianBlur(image, (0, 0), 1)
    return cv2.addWeighted(image, 1.5, blurred, -0.5, 0)


# 4. CLAHE for low-contrast images
def enhance_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced_l = clahe.apply(l_channel)

    enhanced_lab = cv2.merge(
        (enhanced_l, a_channel, b_channel)
    )

    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)


# Calculate PSNR and SSIM
def calculate_metrics(reference, test_image):
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


# Apply the appropriate OpenCV method
def process_image(filename, category):

    original_path = os.path.join(ORIGINAL_DIR, filename)
    degraded_path = os.path.join(DEGRADED_DIR, category, filename)

    original = cv2.imread(original_path)
    degraded = cv2.imread(degraded_path)

    if original is None or degraded is None:
        print(f"Skipping {category}/{filename}: Image not found.")
        return None

    # Match dimensions
    degraded = cv2.resize(
        degraded,
        (original.shape[1], original.shape[0])
    )

    # Select enhancement method
    if category == "blur":
        enhanced = enhance_blur(degraded)

    elif category == "noise":
        enhanced = remove_noise(degraded)

    elif category == "low_resolution":
        enhanced = enhance_low_resolution(degraded)

    elif category == "contrast":
        enhanced = enhance_contrast(degraded)

    else:
        return None

    # Save enhanced image
    output_folder = os.path.join(OUTPUT_DIR, category)
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path, enhanced)

    # Calculate quality metrics
    psnr, ssim = calculate_metrics(original, enhanced)

    print(f"\nCategory: {category}")
    print(f"OpenCV PSNR: {psnr:.4f} dB")
    print(f"OpenCV SSIM: {ssim:.4f}")
    print(f"Saved: {output_path}")

    return {
        "image": filename,
        "category": category,
        "opencv_psnr": psnr,
        "opencv_ssim": ssim
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

            result = process_image(filename, category)

            if result is not None:
                results.append(result)

    if results:

        dataframe = pd.DataFrame(results)

        report_path = os.path.join(
            REPORT_DIR,
            "opencv_metrics.csv"
        )

        dataframe.to_csv(report_path, index=False)

        print("\nOpenCV baseline evaluation completed.")
        print(f"Results saved to: {report_path}")

    else:
        print("No images were processed.")


if __name__ == "__main__":
    main()
