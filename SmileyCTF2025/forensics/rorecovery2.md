🕵️ Challenge Writeup – forensics/rorecovery2

![image](https://github.com/user-attachments/assets/a3148ab8-b14c-47aa-863a-6d99dea70063)

Khi đọc đề, xác nhận yêu cầu của đề là: Tìm name+id của 1 asset ẩn trong file .gz
Form flag:  .;,;.{assetname_id}

Ta có thể dùng lệnh find hoặc exiftool để check kiểu file trước khi làm, nhưng ta có thể phân tích ra được ta sẽ cần check fle nhị phân .
Vì thế dùng lệnh `strings` để check, tôi sẽ để file log.txt ở dưới, nó chính là lệnh strings file .gz
Khi mở lên, tìm kiếm từ khóa id thì có thể thấy rất nhiều đoạn có id: 
![image](https://github.com/user-attachments/assets/bda4aabb-587d-4343-ab46-2853b54637cf)
![image](https://github.com/user-attachments/assets/e7e8efa7-c042-440c-b832-7dfad3615d3c)
![image](https://github.com/user-attachments/assets/34537808-8c93-4453-b3d6-80c8bb4f92e5)

Còn rất nhiều trong file txt nhưng tôi nhận ra rằng các id đều kh có thuộc tính NAME, trừ đoạn này:```PROP%
🔍 Ngoài LegitBase, không đoạn nào khác trong file vừa có cả Name và id, do đó ta xác định được đây là asset ẩn duy nhất cần tìm.
Name
Decal
LegitBase
PROP!
SourceAssetId
PROP
Tags
PROPR
Texture
rbxasset://t
s/SpawnLocation.png
id://137276802718496```

Bạn có thể hiểu PROP chỉ là signiture của code trong Roblox-file .gz này có thể là 1 đoạn dump từ Roblox, cái cần để ý là phần name và id
Đoạn PROP% Name Decal LegitBase cho thấy object có:

Name: LegitBase

Type: Decal (hình dán trong Roblox)
Và đoạn id://137276802718496 chính là Asset ID thật của đối tượng này → đủ để khớp với định dạng flag yêu cầu.

Tóm lại, ta đã có thể thấy asset name là LegitBase và id là 137276802718496 của asset này.
Thử flag vào và done:)))))))

True flag: .;,;.{LegitBase_137276802718496}
