def save_binary_data_to_image(binary_data):
    with open("obrazok.jpg", 'wb') as file:
        file.write(binary_data)
        print("Binary data saved to obrazok.jpg")


def read_binary_file(src):
    with open(src, 'rb') as file:
        binary_data = file.read()
        return binary_data


def append_data_to_file(data):
    with open("obrazok.jpg", 'ab') as file:
        file.write(data)
        print("Data appended to the file.")


def save_data_to_file(data, output_file):
    with open(output_file, 'wb') as file:
        file.write(data)
        print(f"Data saved to {output_file}")

binary_data = read_binary_file("./input/file.jpg")
save_binary_data_to_image(binary_data)

# Oddelovač medzi obrázkom a pridanými dátami
separator = b'EndOfImage'

# Pridanie oddelovača na koniec obrázka
append_data_to_file(separator)

# Pridanie pridaných dát
data_to_append = read_binary_file("./input/code.exe")
append_data_to_file(data_to_append)

# Čítanie zo súboru s oddelovačom
with open("obrazok.jpg", 'rb') as file:
    binary_data = file.read()

# Rozdelenie obrázka a pridaných dát
image_data, added_data = binary_data.split(separator, 1)

# Uloženie pridaných dát do samostatného súboru
save_data_to_file(added_data, "added_data.exe")