
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPORT_DIR = os.path.join(BASE_DIR, "reports")

ai_path = os.path.join(REPORT_DIR, "quality_metrics.csv")
opencv_path = os.path.join(REPORT_DIR, "opencv_metrics.csv")


def main():

    ai_df = pd.read_csv(ai_path)
    opencv_df = pd.read_csv(opencv_path)

    # Combine AI and OpenCV evaluation results
    comparison = pd.merge(
        ai_df,
        opencv_df,
        on=["image", "category"],
        how="inner"
    )

    # Save combined comparison report
    output_path = os.path.join(
        REPORT_DIR,
        "final_comparison.csv"
    )

    comparison.to_csv(output_path, index=False)

    print("\nFINAL RESTORATION COMPARISON")
    print("=" * 65)

    for _, row in comparison.iterrows():

        print(f"\nCategory: {row['category']}")

        print(
            f"Degraded: PSNR={row['degraded_psnr']:.4f}, "
            f"SSIM={row['degraded_ssim']:.4f}"
        )

        print(
            f"OpenCV: PSNR={row['opencv_psnr']:.4f}, "
            f"SSIM={row['opencv_ssim']:.4f}"
        )

        print(
            f"Real-ESRGAN: PSNR={row['restored_psnr']:.4f}, "
            f"SSIM={row['restored_ssim']:.4f}"
        )

    print("\nComparison saved to:", output_path)


if __name__ == "__main__":
    main()
