from PIL import Image
import numpy as np
import os

STOP_MARKER = '1111111111111110'  # Unique binary stop sequence

def text_to_binary(text):
    """Convert text to binary and append stop marker"""
    return ''.join(format(ord(char), '08b') for char in text) + STOP_MARKER

def binary_to_text(binary):
    """Convert binary string back to text, stopping at marker"""
    text = ""
    for i in range(0, len(binary), 8):
        chunk = binary[i:i+8]
        if chunk == STOP_MARKER[:8]:  # If first part of STOP_MARKER is found
            break
        text += chr(int(chunk, 2))
    return text

def hide_text_in_image(image_path, text, output_path):
    """Hide encrypted text inside an image using LSB steganography"""
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    
    binary_text = text_to_binary(text)
    width, height = img.size
    index = 0

    for y in range(height):
        for x in range(width):
            if index < len(binary_text):
                r, g, b = pixels[x, y]
                new_r = (r & ~1) | int(binary_text[index])  # Modify LSB of red channel
                pixels[x, y] = (new_r, g, b)
                index += 1
            else:
                break
        if index >= len(binary_text):  # Stop looping once all bits are hidden
            break

    img_format = os.path.splitext(image_path)[-1]  # Preserve original format
    img.save(f"{output_path}{img_format}")
    print(f"Steganographed image saved as {output_path}{img_format}")

def extract_text_from_image(image_path):
    """Extract hidden text from an image using LSB steganography"""
    img = Image.open(image_path)
    pixels = np.array(img)

    binary_text = ""
    
    for row in pixels:
        for pixel in row:
            binary_text += str(pixel[0] & 1)  # Extract LSB from red channel
            if STOP_MARKER in binary_text:  # Stop as soon as marker is found
                return binary_to_text(binary_text.split(STOP_MARKER)[0])  # Extract only valid text
    
    return "No hidden text found"

