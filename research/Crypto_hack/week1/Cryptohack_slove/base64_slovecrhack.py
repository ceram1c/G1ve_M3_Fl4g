text = '72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf'
base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
encoded=""


a= bytes.fromhex(text)

#chuyển từng giá trị hex thành số nhị phân dạng 8 bit
bit_string = ''.join(f"{byte:08b}" for byte in a)

# thêm số 0 đêm khi thừa bit
while len(bit_string) %6 != 0:
    bit_string+='0'
    
# chia chuỗi nhị phân ban đầu thành từng nhóm 6bit sau đó đối chiếu qua bảng mã base64
for i in range(0, len(bit_string), 6):
    bit=bit_string[i:i+6]
    index = int(bit, 2)
    encoded+=base64[index]
    
print(encoded)


