import cv2
cap = cv2.VideoCapture(0)  # 0 — номер камеры

while True:
    ret, frame = cap.read()  # Читаем кадр
    negative_frame = cv2.bitwise_not(frame)
    cv2.imshow("Веб-камера", negative_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Выход по нажатию 'q'
        break

cap.release()
cv2.destroyAllWindows()
