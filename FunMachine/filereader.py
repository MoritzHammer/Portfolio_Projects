import os

class Reader():
    def __init__(self):
        self.encode_data = []
        self.decode_data = []
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.read_encode_file()
        self.read_decode_file()

    def read_encode_file(self):
        path = f"{self.dir_path}/data_to_encode"
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'r') as f:
                    data = f.read()
                    self.encode_data.append((filename, data))
                    f.close()

    def read_decode_file(self):
        path = f"{self.dir_path}/data_to_decode"
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'r') as f:
                    data = f.read()
                    self.decode_data.append((filename, data))
                    f.close()

    def write_encoded_files(self, files):
        path = f"{self.dir_path}/encoded"
        for filename, data in files:
            with open(f"{path}/{filename}", "w", encoding="UTF-8") as f:
                f.write(data)
                f.close()

    def write_decoded_files(self, files):
        path = f"{self.dir_path}/decoded"
        for filename, data in files:
            with open(f"{path}/{filename}", "w", encoding="UTF-8") as f:
                f.write(data)
                f.close()

    def write_passwords(self, data):
        with open(f"{self.dir_path}/passwords.txt", "w", encoding="UTF-8") as f:
            f.write(data)
            f.close()

