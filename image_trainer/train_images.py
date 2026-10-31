from pathlib import Path
from PIL import Image, ImageOps
import torch
from torchvision import models, transforms
import pandas as pd

SOURCE_DIR = Path(r"C:\StructurePhotos")
OUTPUT_DIR = Path(r"C:\StructurePhotos_Corrected")

MODEL_PATH = "structure_orientation.pth"

CONFIDENCE_THRESHOLD = 0.85

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# Load model
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(
    model.fc.in_features, 4
)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

model.to(device)
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Class = correction required
ROTATIONS = {
    0: 0,
    1: -90,   # Clockwise
    2: 180,
    3: 90     # Counterclockwise
}


def process_photo(image_path):

    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image).convert("RGB")

    tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        predictions = model(tensor)

        probabilities = torch.softmax(
            predictions, dim=1
        )

        confidence, prediction = probabilities.max(1)

    confidence = confidence.item()
    prediction = prediction.item()

    if confidence < CONFIDENCE_THRESHOLD:
        return image, "Manual Review", confidence

    rotation = ROTATIONS[prediction]

    if rotation:
        image = image.rotate(
            rotation,
            expand=True
        )

    status = "Corrected" if rotation else "Already Correct"

    return image, status, confidence


def process_directory():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    extensions = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

    for image_path in SOURCE_DIR.rglob("*"):

        if image_path.suffix.lower() not in extensions:
            continue

        try:
            image, status, confidence = process_photo(image_path)

            if status == "Manual Review":
                results.append({
                    "File": str(image_path),
                    "Status": status,
                    "Confidence": confidence
                })
                continue

            output_path = OUTPUT_DIR / image_path.name

            image.save(output_path, quality=95)

            results.append({
                "File": str(image_path),
                "Status": status,
                "Confidence": confidence
            })

        except Exception as ex:
            results.append({
                "File": str(image_path),
                "Status": f"Error: {ex}",
                "Confidence": None
            })

    pd.DataFrame(results).to_csv(
        OUTPUT_DIR / "orientation_report.csv",
        index=False
    )


if __name__ == "__main__":
    process_directory()

    #train_orientation_model()
    #predict_photo_orientation(image_path)
    #process_photo_directory(directory)