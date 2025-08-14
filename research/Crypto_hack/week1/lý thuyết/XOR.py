text = "KEYXOR"
key=48


# Mã hóa 1 đoạn text bằng XOR nso với 1 key để tạo ra chuỗi ký tự mới
encrypted=""
for c in text:
    encrypted += chr(ord(c)^key)

print(encrypted)

# Giải mã 1 đoạn mã hóa bằng XOR phải có key mới có thế giải mã
decrypted=""
for c in encrypted:
    decrypted += chr(ord(c)^key)
    
print(decrypted)