from Crypto.Cipher import DES


class Encrypt:
    def pkcs7padding(self, text):
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        self.coding = chr(padding)
        return text + padding_text

    def aes_encrypt(self, name, pwd):
        name = name[-4:] + name + "12345678"
        name = name.encode('utf-8')
        cipher = DES.new(name[:8], DES.MODE_ECB)
        content_padding = self.pkcs7padding(pwd)
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        result = encrypt_bytes.hex()
        return result
