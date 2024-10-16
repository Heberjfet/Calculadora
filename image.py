import cv2
import easyocr

# Inicializar el lector en español
reader = easyocr.Reader(['es'])

def capturar_texto_desde_camara():
    # Inicializar la captura de imagen
    video = cv2.VideoCapture(0)

    # Esta variable deberá ser un string de Tkinter
    expresion = ''

    while True:
        ret, frame = video.read()
        if not ret:
            print("Error al capturar el frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        cv2.imshow('Webcam', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # Presionar barra espaciadora para leer texto
            result = reader.readtext(binary)

            for (bbox, text, prob) in result:
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                expresion += text + ' '

            # Muestra el frame con las anotaciones
            cv2.imshow('Webcam', frame)
            cv2.waitKey(500)  # Espera un momento para mostrar el texto capturado

            # Imprime el texto capturado
            print(expresion)

            # Reinicia la expresión
            # En este punto se debe llamar al método que calcula pasandole el string capturado
            video.release()
            cv2.destroyAllWindows()
            return expresion

        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    return expresion