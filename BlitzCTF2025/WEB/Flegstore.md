*FLEG STORE*
<img width="2863" height="1016" alt="image" src="https://github.com/user-attachments/assets/cd7e3aad-8868-47f2-8835-8b4d03f88cf8" />
Bài cho ta một trang web mua bán flag, ta generate coupon rồi redeem để lấy điểm đổi flag. Tuy nhiên giới hạn của coupon có thể gen ra là 5, với giá trị 10 điểm mỗi coupon thì ta sẽ không bao giờ đủ điểm để đổi được flag.
Vậy để có được flag, ta sẽ phải gen ra được nhiều coupon hơn, hoặc sử dụng 1 coupon nhiều lần để đổi đước đủ điểm.
<img width="523" height="256" alt="image" src="https://github.com/user-attachments/assets/f86a1f7f-a7a7-415b-819d-c14d519f8855" />

Dựa vào những thông tin trên, ta biết bài sử dụng lỗ hổng race condition. 
1. Sử dụng burp suit proxy để bắt đc request redeem coupon.
   <img width="1090" height="549" alt="image" src="https://github.com/user-attachments/assets/7cb29def-132a-4c11-bd3d-e0a33b1f5661" />
2. Chuyển sang repeater -> Dùng chức năng send in parallel để gửi nhiều request cùng một lúc
   <img width="1097" height="1130" alt="image" src="https://github.com/user-attachments/assets/f2edd754-d71c-456e-b06e-ae30dd4a81a3" />
   <img width="1390" height="1198" alt="image" src="https://github.com/user-attachments/assets/80f4c712-1a01-409d-b192-8af1bea64a7a" />

Thế là ta thành công có đủ điểm để đổi flag: Blitz{FLEG_L00T3R_SH0P}

