
from PIL import Image, ImageOps
from pathlib import Path

SOURCE_DIR = Path("training/original")
OUTPUT_DIR = Path("training/generated")

ROTATIONS = {
    "0": 0,
    "1": 90,    # Rotate clockwise
    "2": 180,
    "3": 270    # Rotate clockwise
}


def generate_training_images():

    for image_path in SOURCE_DIR.glob("*"):

        try:
            image = Image.open(image_path)
            image = ImageOps.exif_transpose(image).convert("RGB")

            for label, degrees in ROTATIONS.items():

                rotated = image.rotate(
                    -degrees,
                    expand=True
                )

                output_folder = OUTPUT_DIR / label
                output_folder.mkdir(
                    parents=True,
                    exist_ok=True
                )

                output_path = (
                        output_folder /
                        f"{image_path.stem}_{label}.jpg"
                )

                rotated.save(output_path, quality=95)

        except Exception as ex:
            print(f"Error processing {image_path}: {ex}")


if __name__ == "__main__":
    generate_training_images()