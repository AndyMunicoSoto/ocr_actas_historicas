import cv2
import os

# --- CONFIGURACIÓN ---
IMAGEN_PATH = "acta_belaunde_limpia.jpg"
# YOLO exige que el archivo de texto tenga exactamente el mismo nombre que la imagen
TXT_PATH = "acta_belaunde_limpia.txt" 

# --- VARIABLES GLOBALES ---
dibujando = False
ix, iy = -1, -1
clase_actual = 0  # Por defecto empezamos etiquetando la clase 0
imagen = None
imagen_temp = None

# Diccionario para guiarte en la terminal
clases_nombres = {
    0: "0: Nombre del Titular",
    1: "1: Fecha de Nacimiento",
    2: "2: Nombre del Padre",
    3: "3: Nombre de la Madre"
}

def normalizar_yolo(x1, y1, x2, y2, img_w, img_h):
    """Convierte coordenadas de píxeles al formato YOLO (0.0 a 1.0)"""
    # 1. Encontrar el punto central (X, Y)
    centro_x_pix = (x1 + x2) / 2.0
    centro_y_pix = (y1 + y2) / 2.0
    
    # 2. Encontrar ancho y alto absoluto
    ancho_pix = abs(x2 - x1)
    alto_pix = abs(y2 - y1)
    
    # 3. Normalizar dividiendo por las dimensiones totales de la imagen
    centro_x_norm = centro_x_pix / img_w
    centro_y_norm = centro_y_pix / img_h
    ancho_norm = ancho_pix / img_w
    alto_norm = alto_pix / img_h
    
    return (centro_x_norm, centro_y_norm, ancho_norm, alto_norm)

def guardar_caja(clase, x1, y1, x2, y2):
    """Calcula las coordenadas y las agrega al archivo .txt"""
    alto_img, ancho_img = imagen.shape[:2]
    nx, ny, nw, nh = normalizar_yolo(x1, y1, x2, y2, ancho_img, alto_img)
    
    # Usamos "a" (append) para agregar líneas sin borrar las anteriores
    with open(TXT_PATH, "a") as f:
        # Formato YOLO: <clase> <centro_x> <centro_y> <ancho> <alto>
        f.write(f"{clase} {nx:.6f} {ny:.6f} {nw:.6f} {nh:.6f}\n")
    
    print(f"[OK] Caja guardada -> Clase: {clase} | YOLO Coords: {nx:.4f} {ny:.4f} {nw:.4f} {nh:.4f}")

def manejar_raton(event, x, y, flags, param):
    """Detecta los clics y el movimiento del ratón"""
    global ix, iy, dibujando, imagen, imagen_temp, clase_actual

    # Al presionar el clic izquierdo, empezamos a dibujar
    if event == cv2.EVENT_LBUTTONDOWN:
        dibujando = True
        ix, iy = x, y

    # Mientras movemos el ratón con el clic presionado, dibujamos una caja temporal
    elif event == cv2.EVENT_MOUSEMOVE:
        if dibujando:
            imagen_temp = imagen.copy()
            cv2.rectangle(imagen_temp, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('Mini-CVAT', imagen_temp)

    # Al soltar el clic, la caja es definitiva y guardamos
    elif event == cv2.EVENT_LBUTTONUP:
        dibujando = False
        
        # Dibujar en la imagen original para que la caja se quede en pantalla
        cv2.rectangle(imagen, (ix, iy), (x, y), (0, 255, 0), 2)
        # Escribir el número de la clase arribita de la caja
        cv2.putText(imagen, str(clase_actual), (ix, iy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('Mini-CVAT', imagen)
        
        # Mandar a guardar al TXT
        guardar_caja(clase_actual, ix, iy, x, y)


def main():
    global imagen, imagen_temp, clase_actual
    
    # 1. Cargar imagen
    if not os.path.exists(IMAGEN_PATH):
        print(f"Error: No encuentro '{IMAGEN_PATH}'.")
        return
        
    imagen = cv2.imread(IMAGEN_PATH)
    imagen_temp = imagen.copy()
    
    # 2. Crear archivo de texto en blanco si no existe (o limpiarlo si quieres empezar de cero)
    # Si quieres que borre las cajas anteriores cada vez que abres el script, descomenta la siguiente línea:
    # open(TXT_PATH, "w").close()

    # 3. Configurar la ventana interactiva
    cv2.namedWindow('Mini-CVAT', cv2.WINDOW_NORMAL) # Permite redimensionar la ventana si la imagen es muy grande
    cv2.setMouseCallback('Mini-CVAT', manejar_raton)
    
    print("\n" + "="*40)
    print("      INICIANDO MINI-CVAT YOLO")
    print("="*40)
    print("INSTRUCCIONES:")
    print("- Arrastra el ratón para dibujar cajas.")
    print("- Presiona '0', '1', '2' o '3' para cambiar la clase que estás etiquetando.")
    print("- Presiona 'q' o 'ESC' para salir y guardar.")
    print(f"\n[ACTUAL] Estás etiquetando: {clases_nombres[clase_actual]}")
    
    # 4. Bucle principal para escuchar el teclado
    while True:
        cv2.imshow('Mini-CVAT', imagen)
        tecla = cv2.waitKey(1) & 0xFF
        
        # Cambiar de clase con el teclado numérico
        if tecla == ord('0'):
            clase_actual = 0
            print(f"\n[ACTUAL] Cambiaste a: {clases_nombres[clase_actual]}")
        elif tecla == ord('1'):
            clase_actual = 1
            print(f"\n[ACTUAL] Cambiaste a: {clases_nombres[clase_actual]}")
        elif tecla == ord('2'):
            clase_actual = 2
            print(f"\n[ACTUAL] Cambiaste a: {clases_nombres[clase_actual]}")
        elif tecla == ord('3'):
            clase_actual = 3
            print(f"\n[ACTUAL] Cambiaste a: {clases_nombres[clase_actual]}")
            
        # Salir
        elif tecla == ord('q') or tecla == 27: # 27 es la tecla ESC
            break

    cv2.destroyAllWindows()
    print("\n¡Etiquetado finalizado! Revisa tu archivo .txt")

if __name__ == "__main__":
    main()