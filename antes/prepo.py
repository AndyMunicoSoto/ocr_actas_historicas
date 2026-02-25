import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

# Nombre del archivo de imagen que subiste
RUTA_IMAGEN = "acta_belaunde.jpeg"
RUTA_SALIDA = "acta_belaunde_limpia.jpg"

def preprocesar_acta_manuscrita(ruta_entrada, ruta_salida):
    # 1. Verificar si existe la imagen
    if not os.path.exists(ruta_entrada):
        print(f"Error: No se encontró el archivo {ruta_entrada}")
        return

    # 2. Cargar la imagen en ESCALA DE GRISES directamente
    # El '0' indica modo grayscale. Es fundamental para la binarización.
    img_gris = cv2.imread(ruta_entrada, 0)

    # --- FASE DE LIMPIEZA ---

    # 3. Aplicar un ligero Desenfoque Gaussiano (Gaussian Blur)
    # ¿Por qué? El papel viejo tiene mucha textura (granulado). Si binarizamos directo,
    # esa textura se convierte en puntitos negros molestos.
    # Un kernel de (5, 5) suaviza esa textura sin borrar los trazos de la pluma.
    img_suave = cv2.GaussianBlur(img_gris, (5, 5), 0)

    # 4. Binarización Adaptativa (El paso estrella)
    # cv2.adaptiveThreshold calcula el umbral para pequeñas regiones.
    # - blockSize (31): Tamaño del vecindario (debe ser impar). Un valor medio-alto
    #   funciona bien para documentos grandes con letra variable.
    # - C (10): Constante que se resta a la media. Un valor más alto limpia más el fondo
    #   pero puede borrar trazos muy finos. Un valor más bajo conserva más trazos pero deja más ruido.
    #   Probemos con 10 para esta imagen específica.
    img_binarizada = cv2.adaptiveThreshold(
        img_suave,          # Imagen de entrada suavizada
        255,                # Valor máximo (color blanco)
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # Método: media ponderada gaussiana (mejor que la media simple)
        cv2.THRESH_BINARY,  # Tipo: Texto negro sobre fondo blanco
        31,                 # Block Size (ajustable)
        10                  # C (ajustable: prueba entre 5 y 15)
    )

    # 5. Guardar el resultado
    # Esta es la imagen que luego subirías a CVAT para marcar las cajas.
    cv2.imwrite(ruta_salida, img_binarizada)
    print(f"Proceso completado. Imagen limpia guardada en: {ruta_salida}")

    # --- VISUALIZACIÓN (Opcional, para ver el antes y después aquí) ---
    plt.figure(figsize=(14, 8))
    
    plt.subplot(1, 2, 1)
    plt.imshow(img_gris, cmap='gray')
    plt.title('Original (Escala de Grises)')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(img_binarizada, cmap='gray')
    plt.title('Procesada (Adaptativa: Block=31, C=10)')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# --- Ejecutar el script ---
if __name__ == "__main__":
    preprocesar_acta_manuscrita(RUTA_IMAGEN, RUTA_SALIDA)