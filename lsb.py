from PIL import Image
from encryption import encrypt_text, decrypt_text

STOP_MARKER = "1111111111111110"  # Binary stop sequence

def text_to_binary(text):
    """Converts text to binary and appends stop marker"""
    return ''.join(format(ord(char), '08b') for char in text) + STOP_MARKER

def binary_to_text(binary):
    """Converts binary string back to text and stops at marker"""
    text = ""
    for i in range(0, len(binary), 8):
        chunk = binary[i:i+8]
        if chunk == STOP_MARKER[:8]:  # Stop decoding at first part of STOP_MARKER
            break
        text += chr(int(chunk, 2))
    return text

def hide_text_in_image(image_path, text, password, output_path):
    """Encrypts and hides text inside an image using LSB method"""
    print("🔹 Encrypting text...")
    encrypted_text = encrypt_text(password, text)  # Encrypt text
    binary_text = text_to_binary(encrypted_text)  # Convert to binary
    print(f"✅ Text encrypted successfully. Length: {len(binary_text)} bits")

    img = Image.open(image_path).convert("RGB")
    pixels = img.load()

    index = 0
    width, height = img.size
    total_pixels = width * height
    print(f"📷 Image loaded: {image_path} ({width}x{height}, {total_pixels} pixels)")

    if len(binary_text) > total_pixels:
        raise ValueError(f"Insufficient image size. Need {len(binary_text)} pixels, but have {total_pixels}.")

    for y in range(height):
        for x in range(width):
            if index < len(binary_text):
                r, g, b = pixels[x, y]
                new_r = (r & ~1) | int(binary_text[index])  # Modify LSB
                pixels[x, y] = (new_r, g, b)
                index += 1
                if index % 1000 == 0:  # Log every 1000 bits processed
                    print(f"🔄 Processing... {index}/{len(binary_text)} bits embedded")
            else:
                break
        if index >= len(binary_text):  # Stop early when done
            break

    img.save(output_path)
    print(f"✅ Steganographed image saved as {output_path}")

def extract_text_from_image(image_path, password):
    """Extracts and decrypts text hidden inside an image"""
    print("🔹 Extracting text from image...")

    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    binary_text = ""
    
    print(f"📷 Image loaded: {image_path} ({width}x{height})")

    for y in range(height):
        for x in range(width):
            r, _, _ = pixels[x, y]
            binary_text += str(r & 1)
            if binary_text.endswith(STOP_MARKER):  # Stop when marker is found
                break
        if binary_text.endswith(STOP_MARKER):
            break
        if len(binary_text) % 1000 == 0:  # Log every 1000 bits extracted
            print(f"🔄 Extracting... {len(binary_text)} bits read")

    if not binary_text.endswith(STOP_MARKER):
        print("❌ Error: Data is corrupted or incomplete.")
        return "Data is corrupted or incomplete."

    extracted_binary = binary_text.split(STOP_MARKER)[0]
    encrypted_text = binary_to_text(extracted_binary)
    
    print(f"✅ Successfully extracted {len(extracted_binary)} bits. Decrypting now...")
    decrypted_text = decrypt_text(password, encrypted_text)

    print("✅ Text successfully decrypted.")
    return decrypted_text
