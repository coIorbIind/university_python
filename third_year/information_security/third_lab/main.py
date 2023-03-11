import os

from classes import LSBEncodeDecoder


def all_files():
    coder = LSBEncodeDecoder()
    result = []
    for i in range(1, 11):
        filename = f'data/{i}.bmp'
        decoded_data = coder.decode(filename)
        new_filename = 'new_' + filename
        coder.encode(input_filename=filename, output_filename=new_filename, text=decoded_data)
        new_decoded_data = coder.decode(new_filename)
        result.append(new_decoded_data == decoded_data)

    print(result)
    print(all(result))


def main():
    filename = input('Введите название файла для расшифровки: ')
    if not os.path.isfile(filename):
        print('Некорректное имя файла')
        return
    coder = LSBEncodeDecoder()
    decoded_data = coder.decode(filename)
    if not decoded_data:
        print('Не удалось расшифровать файл')
        return
    print('-' * 50)
    print('Расшифрованные данные:', decoded_data)
    print('-' * 50)
    new_filename = 'new_' + filename
    is_encoded = coder.encode(input_filename=filename, output_filename=new_filename, text=decoded_data)
    if not is_encoded:
        print('Не удалось зашифровать файл')
        return
    print('-' * 50)
    print('Проверка:')
    new_decoded_data = coder.decode(new_filename)
    print('Текст из нового файла: ', new_decoded_data)
    print('-' * 50)
    print('Текст совпадает:', new_decoded_data == decoded_data)


if __name__ == '__main__':
    all_files()
    # main()
