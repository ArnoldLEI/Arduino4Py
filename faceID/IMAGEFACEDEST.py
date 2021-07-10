import cv2

face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')
smile_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_smile.xml')

# 設定 Webcam 位置
img = cv2.imread('./image/test.jpg')

# 圖像灰階化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 畫出每一個臉的範圍
faces = face_cascade.detectMultiScale(
    gray,                           #帶檢測圖像，設定灰階可以加快
    scaleFactor=1.1,                #檢測粒度。若粒度增加會加速檢測速度，但會影響準確率
    minNeighbors=10,                 #每隔目標至少要檢測到幾次以上，才被認定是真數據
    minSize=(30, 30),               #數據搜尋的最小尺寸
    flags=cv2.CASCADE_SCALE_IMAGE

)

for (x, y, w, h) in faces:
    cv2.putText(img, 'WOMAN', (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 0), 2)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)
    roi_gray = gray[y:y + h, x:x + w]
    roi_frame = img[y:y + h, x:x + w]
    smile = smile_cascade.detectMultiScale(
        roi_gray,  # 帶檢測圖像，設定灰階可以加快
        scaleFactor=1.1,  # 檢測粒度。若粒度增加會加速檢測速度，但會影響準確率
        minNeighbors=100,  # 每隔目標至少要檢測到幾次以上，才被認定是真數據
        minSize=(30, 30),  # 數據搜尋的最小尺寸
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (sx, sy, sw, sh) in smile:
        cv2.rectangle(roi_frame, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 5)
        cv2.putText(roi_frame, 'smile', (sx, sy - 10), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 0), 2)

print(len(faces), faces)

cv2.imshow('Face', img)
c = cv2.waitKey(0)


