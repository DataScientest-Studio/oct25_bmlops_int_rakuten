import zipfile
from pathlib import Path
from PIL import Image
import pandas as pd
import re

zip_path = Path(r"C:\Users\User\Desktop\MLOps\images.zip")
extract_dir = zip_path.parent / "unzipped_images"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

zip_path = Path(r"C:\Users\User\Desktop\MLOps\images.zip")

# Path to the folder containing the images
image_dir = zip_path.parent / "unzipped_images" / "images" / "image_test"
records = []

# Function to extract product ID from the filename
def extract_product_id(filename):
    match = re.search(r"product_(\d+)", filename)
    return match.group(1) if match else None

# Loop over all JPG images in the folder
for img_file in image_dir.glob("*.jpg"):
    try:
        # Open the image to get width and height
        with Image.open(img_file) as img:
            width, height = img.size

        # Extract product ID directly from the filename
        product_id = extract_product_id(img_file.name)

        if not product_id:
            print(f"️ No product ID found for {img_file.name}")
            continue

        # Append image info to the records list
        records.append({
            "product_id": product_id,
            "path": str(img_file.relative_to(zip_path.parent)),
            "width": width,
            "height": height
        })

    except Exception as e:
        print(f" Error processing {img_file.name}: {e}")

# Path for the output CSV
output_csv = image_dir.parent / "image_metadata.csv"

# Save the records to CSV
pd.DataFrame(records).to_csv(output_csv, index=False)
