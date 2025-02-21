from PIL import Image

def convert_image_to_binary(image_path, output_file, threshold=128):
    # Open the image file
    img = Image.open(image_path)
    
    # Resize the image to fit within the constraints of 512x256
    img = img.resize((512, 256))
    
    # Convert image to grayscale
    img = img.convert('L')
    img.show()
    # Get the size of the image
    width, height = img.size
    width = width // 16
    print(width)
    # Open output file
    with open(output_file, 'w') as f:
        # Write Jack program header
        f.write('// Jack program generated from image\n\nclass output1 {\n')
        f.write('    function int main() {\n        do Screen.setColor(false);\n')
        
        # Loop through each pixel of the image
        for y in range(height):
            for x in range(0,width):
                # Get the pixel value (0-255)
                sum = 0
                a = 1
                k=False
                for i in range(0, 16):
                    pixel_value = img.getpixel((x*16 + i , y))
                    if pixel_value < threshold:
                        if i != 15:
                            sum = sum + a
                        elif sum==0 and i==15:
                            f.write(f'        do Screen.drawPixel({x*16+i}, {y});\n')
                            k=True
                        else:
                            sum = sum - 32768
                    a = a * 2
                
                # Calculate memory address
                mem_address = 16384 + (y * width) + x
                
                # Convert pixel value into Jack statement
                # Assuming white (255) is represented as 0 and black (0) is represented as 1
                # You may need to adjust this depending on how you want to represent colors
                # in your Jack program
                if sum==0 or k:
                    continue
                f.write(f'        do Memory.poke({mem_address}, {sum});\n')
        # Write Jack program footer
        f.write("\n        return 1;\n    }\n}")

# Example usage
input_image = "doctor.png"
output_jack_file = 'output1.jack'
convert_image_to_binary(input_image, output_jack_file, threshold=210)
print(f'Image converted to binary Jack programming language. Output saved to {output_jack_file}')
