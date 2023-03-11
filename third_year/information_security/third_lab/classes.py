import sys


class LSBEncodeDecoder:
    def encode(self, input_filename: str, output_filename: str, text: str):
        bytes_of_text = text.encode()
        text_ind = 0
        try:
            with (
                open(input_filename, mode='rb') as input_file,
                open(output_filename, mode='wb') as output_file,
            ):
                output_file.write(input_file.read(54))
                while temp_pixel := input_file.read(4):
                    if text_ind <= len(bytes_of_text):
                        if text_ind == len(bytes_of_text):
                            data = 0xFF
                        else:
                            data = bytes_of_text[text_ind]
                        encoded_data = 0
                        for i in range(len(temp_pixel)):
                            encoded_data <<= 8
                            encoded_data |= ((temp_pixel[i] & ~(0x3)) | ((data >> 2 * (i)) & 0x3))
                        output_file.write(encoded_data.to_bytes(4, sys.byteorder))
                    else:
                        output_file.write(temp_pixel)
                    text_ind += 1
                return True
        except IOError:
            return False

    def decode(self, file_name: str) -> str | None:
        try:
            with open(file_name, mode='rb') as input_file:
                # Copy headers
                input_file.seek(54)
                result = b''

                while temp_pixel := input_file.read(4):
                    # Extract dd from pixels
                    useful_data = 0
                    for byte_ind in range(len(temp_pixel)):
                        last_bits = temp_pixel[byte_ind] & 0b11
                        modified_bits = last_bits << (6 - 2 * byte_ind)
                        useful_data |= modified_bits

                    # Check end of file
                    if useful_data == 0xFF:
                        break

                    result += useful_data.to_bytes(1, sys.byteorder)
                    
            result = result.decode()

        except IOError:
            result = None

        return result
