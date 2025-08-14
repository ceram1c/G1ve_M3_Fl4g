### ecoded

a= "vnQuyen"

Base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
binary_string =""
encoded=""

# chuyển từng ký tự cảu chuỗi thành nhị phân (dạng 8 bit)
for c in a:
    binary_string += format(ord(c), '08b')


# thêm số 0 đệm khi thừa bit
while len(binary_string) %6 != 0:
    binary_string+='0'

# chia chuỗi nhị phân ban đầu thành từng nhóm 6 bit 
for i in range(0, len(binary_string), 6):
    bit= binary_string[i:i+6]
    index = int(bit, 2)
    encoded+= Base64[index]
    
# thêm padding "="
if (len(a)%3) > 0:
    encoded += "=" * (3-(len(a)%3))
    
print(encoded)


### Decode

binary_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
decode=""

# loại bỏ padding "="
encoded = encoded.rstrip("=")

# chuyển từng ký tự của chuỗi base64 về giá trị index rồi chuyển về dạng nhị phân 6bit
for c in encoded:
    i = Base64.index(c)
    binary_string += format(i, '06b')


# chia chuỗi nhị phân thành từng nhóm 8bit như cũ (1byte)
    
for i in range(0, len(binary_string), 8):
    byte= binary_string[i:i+8]
    if(len(byte)<8):
        break
    decode+=chr(int(byte, 2))
    
print(decode)