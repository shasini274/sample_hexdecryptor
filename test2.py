import binascii
from itertools import combinations

ciphlist = []

class HexDecryptor():

    def __init__(self):
        print("Script Started..")

    def get_extract_hexfile(self):
        print("Extracting Hex File")
        with open('113.hex', 'rb') as file:
            hexChunk = iter(lambda: file.read(1), b'')
            hexCiph = map(binascii.hexlify, hexChunk)

            #each value is extracted from hexCiph and placed in a list
            for hexVal in hexCiph:
                ciphlist.append('0x' + hexVal.decode('utf-8'))

        return ciphlist

    def get_hex_key_pairs(self):
        print("generating 8-bit space key pairs")

        #8 bit space values converted to hex space
        hexlist = [hex(x) for x in range(256)]
        pair = 2
        #All the possible combination of group of two is created
        keyPairList = list(combinations(hexlist, pair))

        return keyPairList

    def dycrypt_cipher(self, keyPairList, cipherList):


        for i, keypair in enumerate(keyPairList):

            plainText = []
            #Each key pair is taken to xor with the cipher text
            for cipInd in range(len(cipherList)):
                #if the index of cipher is even, 2nd key of the key pair is being used to xor
                if cipInd % 2 == 0:
                    plainT = chr(int(cipherList[cipInd], 16) ^ int(keypair[0], 16))
                #if the index of cipher is odd, 1st key of the key pair is being used to xor
                else:
                    plainT = chr(int(cipherList[cipInd], 16) ^ int(keypair[1], 16))

                plainText.append(plainT)
            if plainText[0] == 'L':
                print("%%%%%%%%%%%%%%%%%%%")
                print("Key Pair Instance -> Key1: %s , Key2: %s" % (keypair[0], keypair[1]))
                print("Decrypted Message")
                print(plainText)
                print("%%%%%%%%%%%%%%%%%%%")

if __name__ == '__main__':
    m = HexDecryptor()
    cipherList = m.get_extract_hexfile()
    keyPairList = m.get_hex_key_pairs()
    possiblePlainT = m.dycrypt_cipher(keyPairList, cipherList)