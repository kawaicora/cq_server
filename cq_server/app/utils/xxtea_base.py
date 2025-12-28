import xxtea


xxtea_sign="4meJnPyl"
xxtea_key = "34UFXMgtkz"
def dataDecrypt(encrypted_bytes,xxtea_sign:str,xxtea_key:str):
    decrypt_bytes = xxtea.decrypt(encrypted_bytes[len(xxtea_sign):],xxtea_key)
    return decrypt_bytes
def dataEncrypt(decrypted_bytes,xxtea_sign:str,xxtea_key:str):
    decrypt_bytes = xxtea.encrypt(decrypted_bytes,xxtea_key)
    return xxtea_sign.encode()+decrypt_bytes


