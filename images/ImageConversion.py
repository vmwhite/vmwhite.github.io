from PIL import Image, ImageOps
import os

input_folder = "images/raw"
output_folder = "images/headshots"
target_size = (256, 256)   # (width, height)
target_format = "PNG"     # "PNG" or others
bg_color = (255, 255, 255)       # black padding

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.lower().endswith(("jpg", "jpeg", "png", "bmp", "tiff", "webp")):
        img_path = os.path.join(input_folder, file)
        img = Image.open(img_path).convert("RGB")

        # Resize keeping aspect ratio
        img.thumbnail(target_size, Image.LANCZOS)

        # Rotate image (expand=True ensures full canvas after rotation)
        if file == 'Toni_L_Headshot-1.png':
            img = img.rotate(270, expand=True)


        # Add padding to make it exact size
        img_padded = ImageOps.pad(img, target_size, color=bg_color, centering=(0.5, 0.5))

        new_name = os.path.splitext(file)[0] + ".jpg"
        img_padded.save(os.path.join(output_folder, new_name), target_format)
