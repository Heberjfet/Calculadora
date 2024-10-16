import threading
from tkinter import *
from tkinter import ttk
import math
import speech_recognition as sr
from lexer_parser import lexer, parser
from audio import speak, listen, procesarInstruccion  # Importa las funciones necesarias
from image import capturar_texto_desde_camara  # Importa la función de captura de texto desde la cámara

# Variable global para almacenar el valor en memoria
memoria = None

def click_boton(valor):
    actual = entrada1.get()
    entrada1.set(actual + valor)

def calcular():
    try:
        # Obtener la expresión del cuadro de entrada
        expresion = entrada1.get()
        # Evaluar la expresión usando PLY
        resultado = parser.parse(expresion, lexer=lexer)
        entrada2.set(resultado)
    except Exception as e:
        entrada2.set("Error")

def borrar():
    texto_actual = entrada1.get()
    if texto_actual:
        nuevo_texto = texto_actual[:-1]
        entrada1.set(nuevo_texto)

def borrar_todo():
    entrada1.set("")
    entrada2.set("")

def reconocer_voz():
    expresion = entrada1.get()
    speak("Diga su instrucción")
    while True:
        instruccion = listen()
        if instruccion == "igual":
            speak("Ok, saliendo entonces")
            break
        elif instruccion == "borrar":
            if expresion:
                expresion = expresion[:-1]
                entrada1.set(expresion)
                speak("Último carácter borrado")
            else:
                speak("No hay nada que borrar")
        elif instruccion:
            char = procesarInstruccion(instruccion)
            if char:
                expresion += char
                entrada1.set(expresion)  # Actualiza el Label de entrada con la nueva expresión
                print(f"Expresión actual: {expresion}")
                speak(f"Agregado: {char}")
            else:
                speak("No te entendí")
        else:
            speak("No te entendí")
        # Imprimir la expresión actual después de cada instrucción
        print(f"Cadena del stringVar: {entrada1.get()}")

def iniciar_reconocimiento_voz():
    threading.Thread(target=reconocer_voz).start()

def reconocer_imagen():
    expresion = capturar_texto_desde_camara()
    entrada1.set(expresion)  # Actualiza el Label de entrada con la expresión capturada desde la cámara

# Funciones de memoria
def memoria_guardar():
    global memoria
    memoria = entrada2.get()

def memoria_recuperar():
    if memoria is not None:
        entrada1.set(entrada1.get() + memoria)

def memoria_borrar():
    global memoria
    memoria = None

# Configuración de la interfaz gráfica
root = Tk()
root.title("Calculadora")
root.geometry("+500+80")

estilos = ttk.Style()
estilos.configure('mainframe.TFrame', background="#DBDBDB")

mainframe = ttk.Frame(root, style="mainframe.TFrame")
mainframe.grid(column=0, row=0)

estilos_label1 = ttk.Style()
estilos_label1.configure('label1.TLabel', font="arial 15", anchor="e")

estilos_label2 = ttk.Style()
estilos_label2.configure('label2.TLabel', font="arial 40", anchor="e")

estilos_botones_numeros = ttk.Style()
estilos_botones_numeros.configure('Botones numeros.TButton', font="arial 22", width=5, background="#FFFFFF", relief="flat")

estilos_botones_borrar = ttk.Style()
estilos_botones_borrar.configure('Botones_borrar.TButton', font="arial 22", width=5, relief="flat", background="#CECECE")

estilos_botones_restantes = ttk.Style()
estilos_botones_restantes.configure('Botones restantes.TButton', font="arial 22", width=5, background="#CECECE")

entrada1 = StringVar()
Labelentrada1 = ttk.Label(mainframe, textvariable=entrada1, style="label1.TLabel")
Labelentrada1.grid(column=0, row=0, columnspan=4, sticky=(W, E))

entrada2 = StringVar()
Labelentrada2 = ttk.Label(mainframe, textvariable=entrada2, style="label2.TLabel")
Labelentrada2.grid(column=0, row=1, columnspan=4, sticky=(W, E))

# Botones numéricos
button0 = ttk.Button(mainframe, text="0", style="Botones numeros.TButton", command=lambda: click_boton("0"))
button1 = ttk.Button(mainframe, text="1", style="Botones numeros.TButton", command=lambda: click_boton("1"))
button2 = ttk.Button(mainframe, text="2", style="Botones numeros.TButton", command=lambda: click_boton("2"))
button3 = ttk.Button(mainframe, text="3", style="Botones numeros.TButton", command=lambda: click_boton("3"))
button4 = ttk.Button(mainframe, text="4", style="Botones numeros.TButton", command=lambda: click_boton("4"))
button5 = ttk.Button(mainframe, text="5", style="Botones numeros.TButton", command=lambda: click_boton("5"))
button6 = ttk.Button(mainframe, text="6", style="Botones numeros.TButton", command=lambda: click_boton("6"))
button7 = ttk.Button(mainframe, text="7", style="Botones numeros.TButton", command=lambda: click_boton("7"))
button8 = ttk.Button(mainframe, text="8", style="Botones numeros.TButton", command=lambda: click_boton("8"))
button9 = ttk.Button(mainframe, text="9", style="Botones numeros.TButton", command=lambda: click_boton("9"))

# Otros botones
button_borrar = ttk.Button(mainframe, text=chr(9003), style="Botones_borrar.TButton", command=borrar)
button_borrartodo = ttk.Button(mainframe, text="C", style="Botones_borrar.TButton", command=borrar_todo)
button_parentesis1 = ttk.Button(mainframe, text="(", style="Botones restantes.TButton", command=lambda: click_boton("("))
button_parentesis2 = ttk.Button(mainframe, text=")", style="Botones restantes.TButton", command=lambda: click_boton(")"))
button_punto = ttk.Button(mainframe, text=".", style="Botones restantes.TButton", command=lambda: click_boton("."))

button_division = ttk.Button(mainframe, text=chr(247), style="Botones restantes.TButton", command=lambda: click_boton("/"))
button_multiplicacion = ttk.Button(mainframe, text="X", style="Botones restantes.TButton", command=lambda: click_boton("*"))
button_resta = ttk.Button(mainframe, text="-", style="Botones restantes.TButton", command=lambda: click_boton("-"))
button_suma = ttk.Button(mainframe, text="+", style="Botones restantes.TButton", command=lambda: click_boton("+"))

button_igual = ttk.Button(mainframe, text="=", style="Botones restantes.TButton", command=calcular)
raiz_cuadrada = ttk.Button(mainframe, text="√", style="Botones restantes.TButton", command=lambda: click_boton("math.sqrt("))

button_voz = ttk.Button(mainframe, text="🎤", style="Botones restantes.TButton", command=iniciar_reconocimiento_voz)
button_camera = ttk.Button(mainframe, text="📷", style="Botones restantes.TButton", command=reconocer_imagen)

# Añadir botones para coseno, tangente, logaritmo y porcentaje
button_cos = ttk.Button(mainframe, text="cos", style="Botones restantes.TButton", command=lambda: click_boton("cos("))
button_tan = ttk.Button(mainframe, text="tan", style="Botones restantes.TButton", command=lambda: click_boton("tan("))
button_log = ttk.Button(mainframe, text="log", style="Botones restantes.TButton", command=lambda: click_boton("log("))
button_porcentaje = ttk.Button(mainframe, text="%", style="Botones restantes.TButton", command=lambda: click_boton("/100"))

# Botones de memoria
button_memoria_guardar = ttk.Button(mainframe, text="M+", style="Botones restantes.TButton", command=memoria_guardar)
button_memoria_recuperar = ttk.Button(mainframe, text="MR", style="Botones restantes.TButton", command=memoria_recuperar)
button_memoria_borrar = ttk.Button(mainframe, text="MC", style="Botones restantes.TButton", command=memoria_borrar)

# Orden de los botones en la pantalla
button_parentesis1.grid(column=0, row=2)
button_parentesis2.grid(column=1, row=2)
button_borrartodo.grid(column=2, row=2)
button_borrar.grid(column=3, row=2)

# Fila de botones de tan, cos, log y porcentaje
button_tan.grid(column=0, row=3)
button_cos.grid(column=1, row=3)
button_log.grid(column=2, row=3)
button_porcentaje.grid(column=3, row=3)

button7.grid(column=0, row=4)
button8.grid(column=1, row=4)
button9.grid(column=2, row=4)
button_division.grid(column=3, row=4)

button4.grid(column=0, row=5)
button5.grid(column=1, row=5)
button6.grid(column=2, row=5)
button_multiplicacion.grid(column=3, row=5)

button1.grid(column=0, row=6)
button2.grid(column=1, row=6)
button3.grid(column=2, row=6)
button_suma.grid(column=3, row=6)

button0.grid(column=0, row=7, columnspan=2, sticky=(W, E))
button_punto.grid(column=2, row=7)
button_resta.grid(column=3, row=7)

button_igual.grid(column=0, row=8, columnspan=3, sticky=(W, E))
raiz_cuadrada.grid(column=3, row=8)

# Fila de botones de memoria
button_memoria_guardar.grid(column=0, row=9)
button_memoria_recuperar.grid(column=1, row=9)
button_memoria_borrar.grid(column=2, row=9)

button_voz.grid(column=0, row=10, columnspan=2, sticky=(W, E))
button_camera.grid(column=2, row=10, columnspan=2, sticky=(W, E))

root.mainloop()