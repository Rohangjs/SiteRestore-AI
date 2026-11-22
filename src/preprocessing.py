
import cv2
import numpy as np
import os


# Project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = os.path.join(BASE_DIR, "data", "original")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "degraded")

# Degradation categories
DEGRADATION_TYPES = ["blur", "noise", "low_resolution", "contrast"]


def create_directories():
    """Create folders for each degradation category."""

    for category in DEGRADATION_TYPES:
        folder = os.path.join(OUTPUT_DIR, category)
        os.makedirs(folder, exist_ok=True)


def apply_blur(image):
    """Apply Gaussian blur to simulate loss of sharpness."""

    return cv2.GaussianBlur(image, (9, 9), 2)


def apply_noise(image):
    """Add Gaussian noise to simulate image sensor noise."""

    noise = np.random.normal(0, 20, image.shape)
    noisy_image = image.astype(np.float32) + noise

    return np.clip(noisy_image, 0, 255).astype(np.uint8)


def apply_low_resolution(image):
    """Reduce image resolution and upscale it back."""

    height, width = image.shape[:2]

    small_image = cv2.resize(
        image,
        (width // 4, height // 4),
        interpolation=cv2.INTER_AREA
    )

    return cv2.resize(
        small_image,
        (width, height),
        interpolation=cv2.INTER_LINEAR
    )


def apply_low_contrast(image):
    """Reduce image contrast."""

    return cv2.convertScaleAbs(
        image,
        alpha=0.5,
        beta=60
    )


def process_image(image_path):
    """Generate all four degraded versions of an image."""

    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not read image: {image_path}")
        return

    filename = os.path.basename(image_path)

    degraded_images = {
        "blur": apply_blur(image),
        "noise": apply_noise(image),
        "low_resolution": apply_low_resolution(image),
        "contrast": apply_low_contrast(image)
    }

    for category, degraded_image in degraded_images.items():

        output_folder = os.path.join(OUTPUT_DIR, category)
        output_path = os.path.join(output_folder, filename)

        cv2.imwrite(output_path, degraded_image)

        print(f"Saved: {category}/{filename}")


def main():

    create_directories()

    image_files = [
        file for file in os.listdir(INPUT_DIR)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not image_files:
        print("No input images found.")
        return

    for filename in image_files:

        image_path = os.path.join(INPUT_DIR, filename)

        print(f"\nProcessing: {filename}")

        process_image(image_path)

    print("\nDegradation dataset generated successfully.")


if __name__ == "__main__":
    main()
