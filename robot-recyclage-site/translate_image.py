from PIL import Image

def translate_image(image_path, output_path, y_offset):
    # Open the image
    image = Image.open(image_path)

    # Get the original dimensions
    width, height = image.size

    # Create a new image with the same dimensions and a transparent background
    new_image = Image.new("RGBA", (width, height + y_offset), (255, 255, 255, 0))

    # Paste the original image onto the new image at the specified offset
    new_image.paste(image, (0, y_offset))

    # Save the translated image
    new_image.save(output_path)

# Input and output paths
input_image = "frontend/images/ikrame_taggaa.jpg"
output_image = "frontend/images/ikrame_taggaa_translated.jpg"

# Translate the image down by 50 pixels
y_offset = 50
translate_image(input_image, output_image, y_offset)

print(f"Image translated and saved to {output_image}")