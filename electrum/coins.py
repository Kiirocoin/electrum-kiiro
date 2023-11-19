import sys

class Coin(object):
    @classmethod
    def static_header_offset(cls, height):
        raise Exception('Not implemented')


class Kiiro(Coin):
    PRE_MTP_BLOCKS = 1
    PRE_MTP_HEADER_SIZE = 80
    MTP_HEADER_SIZE = 180
    AFTER_PROGPOW_BLOCK_HEIGHT = 1
    PROGPOW_HEADER_SIZE = 120
    PROGPOW_START_TIME = 1635228000

    @classmethod
    def static_header_offset(cls, height):
        if height > cls.AFTER_PROGPOW_BLOCK_HEIGHT:
            return cls.static_header_offset(cls.AFTER_PROGPOW_BLOCK_HEIGHT) + (height - cls.AFTER_PROGPOW_BLOCK_HEIGHT) * cls.PROGPOW_HEADER_SIZE
        if height > cls.PRE_MTP_BLOCKS:
            return cls.static_header_offset(cls.PRE_MTP_BLOCKS) + (height - cls.PRE_MTP_BLOCKS) * cls.MTP_HEADER_SIZE
        return cls.PRE_MTP_HEADER_SIZE * height

    def get_header_size(self, header: bytes):
        hex_to_int = lambda s: int.from_bytes(s, byteorder='little')
        if hex_to_int(header[68:72]) >= self.PROGPOW_START_TIME: #nTime
            return self.PROGPOW_HEADER_SIZE
        if not (hex_to_int(header[0:4]) & 0x1000): #nVersion
            return self.PRE_MTP_HEADER_SIZE
        return self.MTP_HEADER_SIZE

    @classmethod
    def get_header_size_height(cls, height: int):
        if height >= cls.AFTER_PROGPOW_BLOCK_HEIGHT:
            return cls.PROGPOW_HEADER_SIZE
        if height >= cls.PRE_MTP_BLOCKS:
            return cls.MTP_HEADER_SIZE
        return cls.PRE_MTP_HEADER_SIZE

    def check_header_size(self, header: bytes):
        size = self.get_header_size(header)
        header_len = len(header)
        if header_len == self.PRE_MTP_HEADER_SIZE:
            return True
        if header_len == self.PROGPOW_HEADER_SIZE:
            return True
        if header_len == size:
            return True
        return False

    @classmethod
    def file_size_to_height(cls, fileSize: int):
        preMtpSize = cls.static_header_offset(cls.PRE_MTP_BLOCKS)
        if fileSize <= preMtpSize:
            return fileSize // cls.PRE_MTP_HEADER_SIZE
        preProgpowSize = cls.static_header_offset(cls.AFTER_PROGPOW_BLOCK_HEIGHT)
        if fileSize <= preProgpowSize:
            return cls.PRE_MTP_BLOCKS + (fileSize - preMtpSize) // cls.MTP_HEADER_SIZE
        return cls.AFTER_PROGPOW_BLOCK_HEIGHT + (fileSize - preProgpowSize) // cls.PROGPOW_HEADER_SIZE


class KiiroTestnet(Kiiro):
    PRE_MTP_BLOCKS = 1
    AFTER_PROGPOW_BLOCK_HEIGHT = 37305
    PROGPOW_START_TIME = 1630069200

class KiiroRegtest(Kiiro):
    PRE_MTP_BLOCKS = 2147483647             # INT_MAX 0x7fffffff
    AFTER_PROGPOW_BLOCK_HEIGHT = 2147483647 # INT_MAX 0x7fffffff
    PROGPOW_START_TIME = 2147483647         # INT_MAX 0x7fffffff -- same as electrumX.coins.kiiro.regtest


