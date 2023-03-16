import struct
import sys


def f_func(item):
    x1, x2, x3, x4 = item >> 24, (item >> 16) & 0xff, (item >> 8) & 0xff, item & 0xff
    return ((((S[0][x1] + S[1][x2]) % 2 ** 32) ^ S[2][x3]) + S[3][x4]) % 2 ** 32


def blowfish_encrypt_block(item_64):
    left_32, right_32 = item_64 >> 32, item_64 & 0xffffffff
    for i in range(16):
        left_32 = left_32 ^ P[i]
        right_32 = right_32 ^ f_func(left_32)
        left_32, right_32 = right_32, left_32

    left_32, right_32 = right_32, left_32
    left_32 = left_32 ^ P[17]
    right_32 = right_32 ^ P[16]
    return (left_32 << 32) ^ right_32


def blowfish_decrypt_block(item_64):
    left_32, right_32 = item_64 >> 32, item_64 & 0xffffffff
    for i in range(17, 1, -1):
        left_32 = left_32 ^ P[i]
        right_32 = right_32 ^ f_func(left_32)
        left_32, right_32 = right_32, left_32

    left_32, right_32 = right_32, left_32
    left_32 = left_32 ^ P[0]
    right_32 = right_32 ^ P[1]
    return (left_32 << 32) ^ right_32


def encrypt(message: str):
    arr_of_64bit_numbers = []
    str_bites = message.encode('utf-8')
    for i in range((len(str_bites) + 7) // 8):
        arr_of_64bit_numbers.append(int.from_bytes(str_bites[i * 8:(i + 1) * 8], byteorder=sys.byteorder))

    encr = []
    for i in arr_of_64bit_numbers:
        encr.append(blowfish_encrypt_block(i))
    return encr


def decrypt(encr_message) -> str:
    decr = []
    for i in encr_message:
        decr.append(blowfish_decrypt_block(i))

    decrypt_mes = b''
    for num in decr:
        print(num)
        decrypt_mes += (struct.pack('Q', num))
    return decrypt_mes.decode()


if __name__ == '__main__':
    key = 'my_key'.encode()
    with open('pi.txt') as file:
        text = file.read().replace('\n', '')

    FIXED_P = [int(text[8 * i:8 * (i + 1)], 16) for i in range(18)]
    text = text[8 * 18:]
    FIXED_S = [[int(text[i * 256 * 8 + j * 8:i * 256 * 8 + (j + 1) * 8], 16) for j in range(256)] for i in range(4)]

    P = []
    S = FIXED_S

    k = 0
    for i in range(18):
        long_key = 0
        for j in range(4):
            long_key = (long_key << 8) | key[k % len(key)]
            k += 1
        P.append(FIXED_P[i] ^ long_key)

    data = 0
    for i in range(0, 18, 2):
        data = blowfish_encrypt_block(data)
        P[i] = data >> 32
        P[i + 1] = data % (0x1 << 32)

    for i in range(4):
        for j in range(0, 256, 2):
            data = blowfish_encrypt_block(data)
            S[i][j] = data >> 32
            S[i][j+1] = data % (0x1 << 32)

    #  Запуск
    message = 'Привет!'

    encrypt_message = encrypt(message)
    mes = b''
    for i in encrypt_message:
        mes += (struct.pack('Q', i))

    print(f'Исходный текст - {message}\n')
    print(f'Закодированная последовательность - {mes}\n')
    print(f'Декодированный текст - {decrypt(encrypt_message)}')
