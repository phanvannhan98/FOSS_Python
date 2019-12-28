import os
import cv2
import numpy as np
from PIL import Image

def exportHere():
    # Sử dụng công cụ nhận diện khuôn LBPH nằm trong thư viện OpenCV. ( Trình nhận dạng biểu đồ nhị phân cục bộ )
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'data_face'

    def getImagesWithID(path):
        imagePaths=[os.path.join(path, f) for f in os.listdir(path)]
        faces=[]
        IDs=[]
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID=int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow('training', faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces

    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)
    
    if not os.path.exists('trainer'):
        os.makedirs('trainer')

    recognizer.save('trainer/huanluyen.yml')
    cv2.destroyAllWindows()
