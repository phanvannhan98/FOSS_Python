import numpy as np
import os #Module giúp tương tác với hệ điều hành.
import sqlite3 
import cv2

# Lưu thông tin vào Database.
def SaveUserInfoDB(id, name):
    # connect database
    conn = sqlite3.connect("database.db")

    # Query Tìm ra User có ID nhập vào.
    query = "SELECT * FROM UserInfo WHERE ID="+str(id)

    # Kết quả.
    cursor = conn.execute(query)

    # Kiểm tra tồn tại.
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if isRecordExist==1:
        # Tồn tại thì Update thông tin mới.
        query="UPDATE UserInfo SET Name="+"'"+str(name)+"'"+" WHERE ID="+str(id)
    else:
        # Không tồn tại thì thêm mới.
        query="INSERT INTO UserInfo(ID, Name) VALUES("+str(id)+","+"'"+str(name)+"'"+")"

    conn.execute(query)
    conn.commit()
    conn.close()

def exportHere():
    # Đọc tệp .xml chứa thuật toán và dữ liệu giúp nhận diện khuôn mặt.
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # cv2.VideoCapture(0). Chọn kết nối với Camera của máy. 
    # Nếu tham số là 1 thì chọn Camera thứ 2 được kết nối với máy tính.
    cap = cv2.VideoCapture(0)

    # Nhập thông tin User.
    id = input('ID: ')
    name = input('NAME: ')

    # Kết nối DB thêm hoặc cập nhật thông tin vào DB.
    SaveUserInfoDB(id, name)

    # Tạo biến đếm.
    i = 0

    # Khởi tạo vòng lặp vô hạn để đọc luồng trực tiếp từ máy ảnh.
    while True:
        # Đọc máy ảnh.
        ret, img = cap.read()
        # Chuyển ảnh đọc được từ máy ảnh sang xám.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Sử dụng phương thức detectMultiScale để phát hiện khuôn mặt trong bức ảnh xám.
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            i += 1
            # Tạo thư mục data_face nếu chưa có.
            if not os.path.exists('data_face'):
                os.makedirs('data_face')

            # Lưu ảnh khuôn mặt thu được vào data_face.
            cv2.imwrite('data_face/UserInfo.'+str(id)+"."+str(i)+".jpg",  img[y:y+h,x:x+w])

            # Vẽ hình chữ nhật chứa khuôn mặt lên camera. ( ảnh, Tọa độ bên trái, Tọa độ bên phải, Màu, độ dày ).
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)

        # Show ảnh lên.
        cv2.imshow('Nhan dien khuon mat', img)
        cv2.waitKey(1);

        # Biến đếm > 49 thì dừng lưu ảnh và đóng mọi luồng. ( Lưu 50 tấm mỗi lần. )
        if(i>49):
            cap.release()
            cv2.destroyAllWindows()
            break;

