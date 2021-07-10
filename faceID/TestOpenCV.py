import cv2

#設定 WebCam
cap = cv2.VideoCapture(0)

#設定捕捉區域
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

while True:
    ret, frame = cap.read()
    print(ret, frame)



    cv2.imshow('my video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
