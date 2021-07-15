# your_list = 'abcdefghijklmnopqrstuvwxyz'
# complete_list = []
# for current in range(2):
#     a = [i for i in your_list]
#     for y in range(current):
#         a = [x+i for i in your_list for x in a]
#     complete_list = complete_list+a
#
# print(complete_list)
# from itertools import combinations
#
# hexlist = [hex(x) for x in range(256)]
# r = 2
# ll = list(combinations(hexlist, r))
# print(hexlist)
# print(ll)
# print(ll[0])
# print(ll[0][0])
# print(type(ll[0][0]))

print(hex(int("0x1", 16) ^ int("0x1", 16)))
print(int("0x34", 16) ^ int("0x5f", 16))
print(hex(int("0x34", 16) ^ int("0x5f", 16)))