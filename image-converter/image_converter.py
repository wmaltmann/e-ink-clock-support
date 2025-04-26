from PIL import Image
import os

def image_to_bit_array_1d(path, threshold=0.85):
    # Open the image and convert it to RGB
    image = Image.open(path).convert("RGB")
    
    # Check height only
    if image.height not in (80,16):
        raise ValueError(f"Image {path} must have height 80 pixels, got {image.height}")

    width, height = image.size
    bit_array = []

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            brightness = (r/255 + g/255 + b/255) / 3
            bit_array.append(1 if brightness < threshold else 0)

    return width, bit_array  # Return width too!

def bits_to_hex_string(bit_array):
    padding = (8 - len(bit_array) % 8) % 8
    bit_array += [0] * padding

    byte_list = []
    for i in range(0, len(bit_array), 8):
        byte = 0
        for j in range(8):
            byte |= bit_array[i + j] << (7 - j)
        byte_list.append(byte)

    return ''.join(f'{b:02x}' for b in byte_list)

def generate_constants(image_paths, output_filename, folder :str):
    with open(output_filename, "w") as f:
        f.write("# Auto-generated font data\n\n")
        f.write("FONT_DATA = {\n")  # Start a dict

        for path in image_paths:
            # Get a valid Python constant name (remove extension, make uppercase)
            name = os.path.splitext(os.path.basename(folder+"/"+path))[0]
            const_name = name.upper()

            # Process image
            width, bit_array = image_to_bit_array_1d(folder+"/"+path)
            hex_string = bits_to_hex_string(bit_array)

            # Write entry: width and bitmap
            f.write(f"    '{const_name}': {{'width': {width}, 'bitmap': '{hex_string}'}},\n")

        f.write("}\n")  # Close dict

# 80px font
filename = "80/digital_font_80.py"
folder = "80"
image_files = ["0.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "space.jpg", "colon.jpg"]

generate_constants(image_files, filename, folder)
