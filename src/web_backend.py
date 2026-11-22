
import cv2
import numpy as np
import time
import sys
import subprocess
import tempfile

from pathlib import Path

from src.opencv_baseline import (
    enhance_blur,
    remove_noise,
    enhance_low_resolution,
    enhance_contrast
)


# ==========================================================
# OPENCV RESTORATION
# ==========================================================

def restore_with_opencv(uploaded_image, category):
    """
    Restore an uploaded image using existing OpenCV algorithms.

    Args:
        uploaded_image: Image bytes received from Streamlit.
        category: blur, noise, low_resolution, or contrast.

    Returns:
        restored_image_bytes, processing_time
    """

    image_array = np.frombuffer(uploaded_image, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError(
            "Invalid image. Unable to decode the uploaded file."
        )

    restoration_methods = {
        "blur": enhance_blur,
        "noise": remove_noise,
        "low_resolution": enhance_low_resolution,
        "contrast": enhance_contrast
    }

    if category not in restoration_methods:
        raise ValueError(
            f"Unsupported degradation category: {category}"
        )

    start_time = time.perf_counter()

    restored_image = restoration_methods[category](image)

    processing_time = time.perf_counter() - start_time

    success, encoded_image = cv2.imencode(
        ".png",
        restored_image
    )

    if not success:
        raise RuntimeError(
            "Unable to encode the restored image."
        )

    return encoded_image.tobytes(), processing_time


# ==========================================================
# REAL-ESRGAN RESTORATION
# ==========================================================

def restore_with_realesrgan(uploaded_image):
    """
    Restore an uploaded image using Real-ESRGAN x4plus.

    Args:
        uploaded_image: Image bytes received from Streamlit.

    Returns:
        restored_image_bytes, processing_time
    """

    # Locate project directories

    project_root = Path(__file__).resolve().parent.parent

    realesrgan_dir = project_root / "Real-ESRGAN"

    inference_script = (
        realesrgan_dir / "inference_realesrgan.py"
    )

    weights_path = (
        realesrgan_dir / "weights" / "RealESRGAN_x4plus.pth"
    )

    # Check required files

    if not realesrgan_dir.exists():
        raise FileNotFoundError(
            f"Real-ESRGAN directory not found: {realesrgan_dir}"
        )

    if not inference_script.exists():
        raise FileNotFoundError(
            f"Real-ESRGAN inference script not found: {inference_script}"
        )

    if not weights_path.exists():
        raise FileNotFoundError(
            f"Real-ESRGAN model weights not found: {weights_path}"
        )

    start_time = time.perf_counter()

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        input_path = temp_path / "uploaded_image.png"

        output_dir = temp_path / "restored"

        output_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded image temporarily

        input_path.write_bytes(uploaded_image)

        # Real-ESRGAN inference command

        command = [
            sys.executable,
            str(inference_script),
            "-n", "RealESRGAN_x4plus",
            "-i", str(input_path),
            "-o", str(output_dir),
            "--model_path", str(weights_path),
            "--fp32",
            "-t", "256"
        ]

        # Execute Real-ESRGAN

        try:

            result = subprocess.run(
                command,
                cwd=str(realesrgan_dir),
                capture_output=True,
                text=True,
                timeout=600,
                check=False
            )

        except subprocess.TimeoutExpired:
            raise TimeoutError(
                "Real-ESRGAN processing exceeded 10 minutes. "
                "Try a smaller input image."
            )

        except Exception as error:
            raise RuntimeError(
                f"Unable to execute Real-ESRGAN: {error}"
            )

        # Check inference result

        if result.returncode != 0:

            raise RuntimeError(
                "Real-ESRGAN restoration failed:\n"
                + result.stderr[-3000:]
                + "\n"
                + result.stdout[-1000:]
            )

        # Find generated output image

        restored_files = (
            list(output_dir.glob("*.png"))
            + list(output_dir.glob("*.jpg"))
            + list(output_dir.glob("*.jpeg"))
        )

        if not restored_files:

            raise FileNotFoundError(
                "Real-ESRGAN finished, but no restored image "
                "was generated. Check the inference script output."
            )

        # Read restored image

        restored_path = restored_files[0]

        restored_image_bytes = restored_path.read_bytes()

    processing_time = time.perf_counter() - start_time

    return restored_image_bytes, processing_time
