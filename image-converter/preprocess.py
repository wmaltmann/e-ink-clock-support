import os
import importlib.util
import pprint

def _hex_string_to_bit_array(hex_string):
    bit_array = []
    for i in range(0, len(hex_string), 2):
        byte = int(hex_string[i:i+2], 16)
        for j in range(8):
            bit_array.append((byte >> (7 - j)) & 1)
    return bit_array

def _hex_string_to_bytes(hex_string):
    return bytes(int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2))

def preprocess_font(font):
    processed = {'height': font['height']}
    for char, data in font.items():
        if char == 'height':
            continue
        bitmap_bytes = _hex_string_to_bytes(data['bitmap'])
        processed[char] = {
            'width': data['width'],
            'bitmap_bytes': bitmap_bytes,
        }
    return processed

def load_font_module(font_path, var_name):
    spec = importlib.util.spec_from_file_location("font_module", font_path)
    font_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(font_module)
    return getattr(font_module, var_name)

def save_preprocessed_font(processed_font, output_path, output_var="FONT_PRE"):
    with open(output_path, "w") as f:
        f.write(f"{output_var} = ")
        f.write(repr(processed_font))
        f.write("\n")

def main():
    input_font_py = "18/franklin_18.py"
    # input_font_py = "80/DIGITAL_80.py"  
    temp = input_font_py.split("/")[1]
    font_var_name = temp.split(".")[0].upper()
    output_py = temp.split(".")[0] + "_pre.py"
    output_var_name = temp.split(".")[0].upper() + "_PRE"

    font = load_font_module(input_font_py, font_var_name)
    processed = preprocess_font(font)
    save_preprocessed_font(processed, output_py, output_var_name)
    print(f"Preprocessed font saved to {output_py}")

if __name__ == "__main__":
    main()
