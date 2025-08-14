# XOR (exclusive or) 
- XOR là 1 trong những phép toán trên thao tác bit, được thực hiện trên 1 hoặc nhiều chuỗi bit hoặc số nhị phân.
- XOR lấy 2 dãy bit có cùng độ dài, thực hiện trên mỗi cặp bit tương ứng. Trả về 1 nếu 1 trong 2 bit tương ứng của 2 số là 1, còn trả về 0 khi cả 2 bit tương ứng bằng nhau.
'''
    A   |   B   |   A XOR B
    0   |   0   |   0       
    1   |   0   |   1
    0   |   1   |   1
    1   |   1   |   0
    '''
- nói đơn giản XOR sẽ trả về 1 nếu 2 bit tương ứng khác nhau, trả về 0 nếu 2 bit giống nhau 

### Tính chất 
- Giao hoán: "A ⊕ B = B ⊕ A" ==> cách sắp xếp 2 đầu vào không cần thứ tự
- Kết hợp: "A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C" ==> trong phép XOR có thể nối lại với nhau và thứ tự không quan trọng
- Bất kỳ giá trị nào XOR với 0 sẽ không thay đổi
- Ngược lại, Bất kỳ giá trị nào XOR với 1 sẽ đảo ngược dãy bit
'''
101110 ^ 0 = 101110 //46
101110 ^ 1 = 010001 //17
'''
- Bât Bất kỳ giá trị nào được XOR chính nó sẽ bằng 0  "101110 ^ 101110 = 000000"

