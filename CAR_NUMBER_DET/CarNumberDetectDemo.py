import cv2

img = cv2.imread('./image/car1.png')
cardect = cv2.CascadeClassifier('./xml/tw.xml')


# 圖像灰階化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cars = cardect.detectMultiScale(
        gray,                           #帶檢測圖像，設定灰階可以加快
        scaleFactor=1.1,                #檢測粒度。若粒度增加會加速檢測速度，但會影響準確率
        minNeighbors=8,                 #每隔目標至少要檢測到幾次以上，才被認定是真數據
        minSize=(60, 60),               #數據搜尋的最小尺寸
        flags=cv2.CASCADE_SCALE_IMAGE

    )




# 在臉部周圍畫矩形框
for (x, y, w , h) in cars:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

cv2.imshow('My Video', img)

cv2.waitKey(0)


# 釋放資源

cv2.destroyAllWindows()




