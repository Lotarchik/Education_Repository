import cv2


def draw_whiskers(image_path):
    img = cv2.imread(image_path)

    # Загрузка каскада для обнаружения кошачьих лиц
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalcatface_extended.xml')

    # Конвертация в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Обнаружение кошачьих лиц
    # Если не обнаруживает морды:

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,  # Уменьшить для лучшего поиска
        minNeighbors=3,  # Уменьшить для большей чувствительности
        minSize=(50, 50)  # Уменьшить для маленьких морд
    )

    for (x, y, w, h) in faces:
        # Рассчитываем центр морды
        center_x = x + w // 2
        center_y = y + h // 2

        # Параметры усов
        whisker_length = w // 2
        whisker_y = center_y + h // 4  # Смещение вниз от центра

        # Рисуем усы
        # Левые усы
        cv2.line(img, (center_x, whisker_y),
                 (center_x - whisker_length, whisker_y - 15),
                 (0, 0, 255), 2)
        cv2.line(img, (center_x, whisker_y),
                 (center_x - whisker_length, whisker_y),
                 (0, 0, 255), 2)
        cv2.line(img, (center_x, whisker_y),
                 (center_x - whisker_length, whisker_y + 15),
                 (0, 0, 255), 2)

        # Правые усы
        cv2.line(img, (center_x, whisker_y),
                 (center_x + whisker_length, whisker_y - 15),
                 (0, 0, 255), 2)
        cv2.line(img, (center_x, whisker_y),
                 (center_x + whisker_length, whisker_y),
                 (0, 0, 255), 2)
        cv2.line(img, (center_x, whisker_y),
                 (center_x + whisker_length, whisker_y + 15),
                 (0, 0, 255), 2)

    # Показать и сохранить результат
    cv2.imshow('Cat with Whiskers', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Сохранение результата
    cv2.imwrite('output_with_whiskers.jpg', img)
    print("Изображение сохранено как output_with_whiskers.jpg")


# Использование функции
draw_whiskers('cats.jpeg')
