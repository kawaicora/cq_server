
from app.utils.Magic import *
import random
import os
import struct
class Ec2b:
    def __init__(self):
        self.key = None
        self.data = None
        self.temp = None
        self.seed = None
        

    
    @staticmethod
    def SetSeed(seed):
        random.seed(seed)
        temp = bytearray(4096)
        for i in range(4096 // 8):
            random_bytes = random.getrandbits(64).to_bytes(8, byteorder='little')
            struct.pack_into('<Q', temp, i * 8, int.from_bytes(random_bytes, byteorder='little'))
        return temp
    @staticmethod
    def GetSeed(key, data):
        v = ~ 0xCEAC3B5A867837AC & 0xFFFFFFFFFFFFFFFF
        # v = ^uint32(0xCEAC3B5A867837AC)
        # v=0x3153c4a57987c853
        v = v ^ struct.unpack("<Q", key[:8])[0]
        v = v ^ struct.unpack("<Q", key[8:])[0]
        for i in range(0, len(data) // 8):
            chunk = data[i*8:(i+1)*8]
            v = v ^ struct.unpack("<Q", chunk)[0]
        return v
    @staticmethod
    def LoadKey(data):
        if len(data) < 4+4+16+4+2048:
            return b"",b""
        if data[:4] != b"Ec2b":
            return b"",b""

        key_len = struct.unpack("<I", data[4:8])[0]
        if key_len != 16:
            return b"",b""

        data_len = struct.unpack("<I", data[24:28])[0]
        if data_len != 2048:
            return b"",b""

        key = data[8:24]
        data = data[28:28+2048]
        return key,data
    
    
    @staticmethod
    def GetKey(key, data):
        if len(key) != 16 or len(data) != 2048:
            return b""

        result = b"Ec2b"
        result += struct.pack("<I", len(key))
        result += key
        result += struct.pack("<I", len(data))
        result += data

        return result


    def CreateKey():
        key_len = 16
        data_len = 2048

        # 生成随机的 key 和 data
        key = os.urandom(key_len)
        data = os.urandom(data_len)
        nkey = bytearray(key)
        Ec2b.KeyScramble(nkey)

        key = bytes(nkey)
        # 构造 Ec2b 数据格式
        result = b"Ec2b"
        result += struct.pack("<I", len(key))
        result += key
        result += struct.pack("<I", len(data))
        result += data

        return result



    @staticmethod
    def KeyScramble(key):
        roundKeys = [[0] * 16 for _ in range(11)]
        
        for r in range(11):
            for i in range(16):
                for j in range(16):
                    idx = (r << 8) + (i << 4) + j
                    roundKeys[r][i] ^= aesXorTable[1][idx] ^ aesXorTable[0][idx]
        
        Ec2b.XorRoundKey(key, roundKeys[0])
        
        for r in range(1, 10):
            Ec2b.SubBytesInv(key)
            Ec2b.ShiftRowsInv(key)
            Ec2b.MixColsInv(key)
            Ec2b.XorRoundKey(key, roundKeys[r])
        
        Ec2b.SubBytesInv(key)
        Ec2b.ShiftRowsInv(key)
        Ec2b.XorRoundKey(key, roundKeys[10])
        
        for i in range(16):
            key[i] ^= keyXorTable[i]
    @staticmethod
    def XorRoundKey(key, roundKey):
        for i in range(16):
            key[i] ^= roundKey[i]

    @staticmethod
    def SubBytes(key):
        for i in range(16):
            key[i] = lookupSbox[key[i]]
    @staticmethod
    def SubBytesInv(key):
        for i in range(16):
            key[i] = lookupSboxInv[key[i]]
    @staticmethod
    def ShiftRows(key):
        temp = bytearray(key)
        for i in range(16):
            key[i] = temp[shiftRowsTable[i]]
    @staticmethod
    def ShiftRowsInv(key):
        temp = bytearray(key)
        for i in range(16):
            key[i] = temp[shiftRowsTableInv[i]]
    @staticmethod
    def MixColsInv(key):
        for i in range(0, 16, 4):
            a0, a1, a2, a3 = key[i], key[i + 1], key[i + 2], key[i + 3]
            key[i] = lookupG14[a0] ^ lookupG9[a3] ^ lookupG13[a2] ^ lookupG11[a1]
            key[i + 1] = lookupG14[a1] ^ lookupG9[a0] ^ lookupG13[a3] ^ lookupG11[a2]
            key[i + 2] = lookupG14[a2] ^ lookupG9[a1] ^ lookupG13[a0] ^ lookupG11[a3]
            key[i + 3] = lookupG14[a3] ^ lookupG9[a2] ^ lookupG13[a1] ^ lookupG11[a0]
    @staticmethod
    def Xor(data, key):
        result = bytearray()
        for i in range(len(data)):
            result.append(data[i] ^ key[i % len(key)])
        return result