from PIL import Image

def encode_message(image_path, message, output_image_path):
    # Open the image
    image = Image.open(image_path)
    pixels = list(image.getdata())

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Use a delimiter to mark the end of the message

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message is too long to be hidden in the image.")

    # Modify pixels to hide the binary message
    new_pixels = []
    message_index = 0

    for pixel in pixels:
        new_pixel = []
        for color_value in pixel[:3]:  # Modify RGB values only
            if message_index < len(binary_message):
                # Replace the LSB with the next bit of the message
                new_color_value = color_value & ~1 | int(binary_message[message_index])
                new_pixel.append(new_color_value)
                message_index += 1
            else:
                new_pixel.append(color_value)
        if len(pixel) == 4:  # Handle alpha channel if present
            new_pixel.append(pixel[3])
        new_pixels.append(tuple(new_pixel))

    # Create a new image with modified pixels
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    new_image.save(output_image_path)
    print(f"Message encoded and saved to {output_image_path}")

def decode_message(image_path):
    # Open the image
    image = Image.open(image_path)
    pixels = list(image.getdata())

    binary_message = ""
    for pixel in pixels:
        for color_value in pixel[:3]:  # Only extract from RGB values
            binary_message += str(color_value & 1)

    # Split binary string into 8-bit chunks and convert to ASCII
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '11111110':  # Check for the end-of-message delimiter
            break
        message += chr(int(byte, 2))

    return message
if __name__ == "__main__":
    input_image = "C:\\Users\\arjun\\OneDrive\\Documents\\lsb_steganography\\Philips.jpg"
    output_image = "C:\\Users\\arjun\\OneDrive\\Documents\\lsb_steganography\\encoded_image.png"
    secret_message = input("Enter the message : ")

    # Encode the message into the image
    encode_message(input_image, secret_message, output_image)

    # Decode the message from the image
    decoded_message = decode_message(output_image)
    print("Decoded message:", decoded_message)
