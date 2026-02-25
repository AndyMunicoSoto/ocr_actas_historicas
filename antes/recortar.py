import cv2

# 1. Cargar la imagen para obtener sus dimensiones reales en píxeles
img = cv2.imread("dataset_actas/train/images/acta_belaunde_limpia.jpg")
alto_img, ancho_img = img.shape[:2]

print(f"Dimensiones de la imagen: {ancho_img}px de ancho x {alto_img}px de alto\n")

# 2. Tus coordenadas YOLO exactas
coordenadas_yolo = [
    [0, 0.193612, 0.066250, 0.229495, 0.107500],
    [1, 0.216483, 0.134375, 0.205836, 0.033750],
    [2, 0.652997, 0.138750, 0.258675, 0.035000]
]

# 3. La matemática inversa para cada caja
for caja in coordenadas_yolo:
    clase = int(caja[0])
    x_centro_norm = caja[1]
    y_centro_norm = caja[2]
    ancho_norm = caja[3]
    alto_norm = caja[4]

    # A) Convertir porcentajes a píxeles reales
    x_centro = x_centro_norm * ancho_img
    y_centro = y_centro_norm * alto_img
    ancho_px = ancho_norm * ancho_img
    alto_px = alto_norm * alto_img

    # B) Calcular las esquinas (x1, y1) superior izquierda y (x2, y2) inferior derecha
    x1 = int(x_centro - (ancho_px / 2))
    y1 = int(y_centro - (alto_px / 2))
    x2 = int(x_centro + (ancho_px / 2))
    y2 = int(y_centro + (alto_px / 2))

    print(f"--- Clase {clase} ---")
    print(f"Coordenadas OpenCV: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

    # C) Recortar la imagen (Recuerda que en Numpy/OpenCV primero va Y, luego X)
    recorte = img[y1:y2, x1:x2]
    
    # Guardar el pedacito de imagen
    nombre_archivo = f"recorte_clase_{clase}.jpg"
    cv2.imwrite(nombre_archivo, recorte)
    print(f"¡Guardado: {nombre_archivo}!")

print("\n¡Proceso terminado! Revisa tu carpeta.")