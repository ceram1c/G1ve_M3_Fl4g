# XOR Starter

'''
string = 'label'
for c in string:
    c = chr(ord(c)^13)
    print(c+"", end="")
'''


# XOR Properties

'''
# tạo 1 func để duyệt qua và xor từng bit của 2 dãydãy
def xor_byte(a, b):
    return bytes(x^y for x, y in zip(a, b))

KEY1 = 'a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313'
KEY2xorKEY1 = '37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e'
KEY2xorKEY3 = 'c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1'
FLAGxorKEY1xorKEY3xorKEY2 = '04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf'

# chuyển về dạng hex
KEY1 = bytes.fromhex(KEY1)
KEY2xorKEY1 = bytes.fromhex(KEY2xorKEY1)
KEY2xorKEY3 = bytes.fromhex(KEY2xorKEY3)
FLAGxorKEY1xorKEY3xorKEY2 = bytes.fromhex(FLAGxorKEY1xorKEY3xorKEY2)

# thực hiện XOR để tìm KEY2, KEY3 sau đó là tới FLAG
KEY2 = xor_byte(KEY2xorKEY1, KEY1)
KEY3 = xor_byte(KEY2xorKEY3, KEY2)
FLAG = xor_byte(xor_byte(xor_byte(FLAGxorKEY1xorKEY3xorKEY2, KEY1), KEY2), KEY3)
print(FLAG.decode('utf-8'))
'''


# Favourite byte

'''
string = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'
xor= bytes.fromhex(string)

# xor đoạn mã với từng giá trị byte để dò tìm byte đúng
for i in range(1, 256):
    text = bytes(b^i for b in xor)
    flag = "".join(chr(b) for b in text)
    # nếu flag xor ra bắt đầu từ fromat "crypto{}" thì ngay lập tức break vòng lặp và trả về flag
    if flag.startswith("crypto"):
        break
print(flag)
'''


# You either know, XOR you don't

'''
string = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
a='myXORkey'
xor= bytes.fromhex(string)
key = bytes(a, 'utf-8')
# xor từng ký tự của dãy mã với lần lượt các ký tự của key, khi hết key thì lặp lại cho tới khi hết ký tự của đoạn mã
text = bytes([b ^ key[i%len(key)] for i, b in enumerate(xor)])
print(text)
'''
