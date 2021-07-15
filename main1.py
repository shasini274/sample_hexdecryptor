import binascii
import codecs
# from intelhex import IntelHex
# ih = IntelHex()
# ih = IntelHex('113.hex')
# pydict = ih.todict()
# print(ih)
# print(ih.loadhex('113.hex'))
# print(ih.loadfile('113.hex', format='hex'))
# with open('113.hex', 'r', newline='') as file:
#     print(file.read())
#
# with open('113.txt', 'r', newline='') as file1:
#     print(file1.read())

# class HexFile(object):
#     def __init__(self, fp, wordsize=16):
#         self.fp = fp
#         self.ws = wordsize
#     def __iter__(self):
#         while True:
#             data = self.fp.read(self.ws)
#             if not data: break
#             yield data.hex()
#
#
# if __name__ == '__main__':
#     f = HexFile(open('113.hex', 'rb'))
#     for hexword in f:
#         print(hexword)
#         print("*")
#         print(int(hexword, 16))
#         # print(hexword.decode())
#         print("%")
#
# s = open('113.hex', 'rb').read()
# print(s)
list = []
with open("113.hex", "rb") as f:
    while (byte1 := f.read(16)):
        print(byte1)
        print(type(byte1))
        list.append(byte1.hex())
        print(byte1.hex())
print(list)
# listt = []
# with open('113.hex', 'rb') as f:
#     for chunk in iter(lambda: f.read(1), b''):
#         print(chunk)
#         listt.append(chunk.decode('UTF-8'))
#         # listt = listt + codecs.encode(chunk, 'hex')
#         # print(codecs.encode(chunk, 'hex'))
# print(listt)
