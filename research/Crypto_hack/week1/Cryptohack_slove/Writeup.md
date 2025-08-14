# Base64

![image](https://github.com/user-attachments/assets/942ec7d9-ddf7-47c2-a74e-7005bc43a65c)

bài này cho ta 1 đoạn mã hex và yêu cầu chuyển nó về dạng byte rồi encoded dưới dạng base64.
sử dụng python để code 1 đoạn encoded base64:

  ```py
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
  ```
![image](https://github.com/user-attachments/assets/ef33416f-d71d-4604-b838-74c927374751)


# XOR Starter

![image](https://github.com/user-attachments/assets/d7b05653-8fe5-4f2d-b5a9-d1daa84feb99)

yêu cầu của bài là muốn chúng ta XOR 1 chuỗi "label" với 13, sau đó chuyển lại về dạng string để nộp.
Code python giải bài:

```py
string = 'label'

for c in string:
    c = chr(ord(c)^13)
    print(c+"", end="")
```

![image](https://github.com/user-attachments/assets/1d0b121b-f5c0-4626-9814-429c331079d5)


# XOR Properties

![image](https://github.com/user-attachments/assets/1d6756d2-04da-45a3-b5c5-cde9c1128574)

flag của bài này đã được xor với 3 key ngẫu nhiên khác nhau, 2 key còn lại cũng bị tương tự chỉ còn key 1

ta sử dụng tính chất "A ^ B = C | C ^ B = A" từ đó có thể tính ra được lần lượt các key 2, key 3 rồi tới flag

- đầu tiên chuyển 3 đoạn mã về lại dạng hex rồi thực hiện việc xor từ bit của 2 dãy 1 để tìm ra key2, key3, rồi tới flag



Code python giải bài:
```py
# tạo 1 func để duyệt qua và xor từng bit của 2 dãy
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
```

![image](https://github.com/user-attachments/assets/133e35ba-588f-4e29-9b58-c817cfa41db1)



#  Favourite byte

![image](https://github.com/user-attachments/assets/513f98e5-2516-45ac-9e4b-eeb1b6542fd2)

đoạn mã của bài này là flag được XOR với 1 byte đơn lẻ duy nhất nhưng không được cho biết
1 single byte có thể chứ 256 giá trị khác nhau bất kỳ, tận dụng điều đó ta là 1 vòng lặp duyệt từng giá trị từ 1-->256 và XOR ngược đoạn mã với nó để để tìm flag, nếu kết quá bắt đầu theo form "crypto{" thì break và trả giá trị  

Code python giải bài:
```py
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
```

![image](https://github.com/user-attachments/assets/d48917de-e831-4919-a279-48bb10ac5ddc)




# You either know, XOR you don't

![image](https://github.com/user-attachments/assets/c61dda33-1ca0-4fa0-97b9-822802646e99)


đoạn mã theo như bài ra đã được XOR với 1 KEY secret. Tương tự với tính chất "A ^ B = C | C ^ A = B".
Thì ta có thể hiểu rằng "Flag ^ Key = cipher | cipher ^ Key = Flag".
1 ví dụ tương tự:

![image](https://github.com/user-attachments/assets/a958ffd7-555d-4955-bcc7-ef9fa0b2d0ae)

ta xor flag "Flag2808{H3110}" với 1 key "Secret" sẽ có được 1 đoạn kết qua từ phép xor

![image](https://github.com/user-attachments/assets/1b7d8ee4-9ca3-4365-939f-6196ec71e7a8)

tiếp tục xor kết quả với flag từ trước ta sẽ nhận được 1 đoạn "secret" là key ban dầu của phép tính

### ==> key ^ flag = cipher | cipher ^ flag = key

áp dụng từ ví dụ trên ta sử dụng đoạn mã bài cho xor với flag có form "crypto{" để tìm key ban đầu 

![image](https://github.com/user-attachments/assets/b9758e14-6dab-4c6d-b7aa-e3bd6b74400e)

từ kết quả ta có thể guess rằng key của bài là "myXORkey" để giải bài này

Code python giải bài:
```py
string = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
a='myXORkey'
xor= bytes.fromhex(string)
key = bytes(a, 'utf-8')
# xor từng ký tự của dãy mã với lần lượt các ký tự của key, khi hết key thì lặp lại cho tới khi hết ký tự của đoạn mã
text = bytes([b ^ key[i%len(key)] for i, b in enumerate(xor)])
print(text)
```

![image](https://github.com/user-attachments/assets/dd9ff35f-f546-4c2e-b4aa-c7cbcaa6eb31)













