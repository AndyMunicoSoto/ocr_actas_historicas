import easyocr
import glob
import os
import cv2
import numpy as np

# Función de preprocesamiento para mejorar el contraste
def preprocesar_imagen(ruta_imagen):
    # Cargar la imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    
    # Aumentar el contraste (Opcional: ajustar los valores según tus imágenes)
    # Se puede usar ecualización de histograma o ajuste de brillo/contraste
    img_contraste = cv2.equalizeHist(img)
    
    # Opcional: Binarización para dejar solo blanco y negro
    # _, img_binaria = cv2.threshold(img_contraste, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return img_contraste # Retornamos la imagen procesada

print("Cargando el motor de EasyOCR en Español...")
lector = easyocr.Reader(['es'])

archivos_recortes = glob.glob("imprenta.jpeg")

print("\n" + "="*50)
print(" INICIANDO EXTRACCIÓN CON EASY-OCR (CON PREPROCESAMIENTO)")
print(f" Imágenes encontradas: {len(archivos_recortes)}")
print("="*50)

if len(archivos_recortes) == 0:
    print("❌ No se encontraron recortes.")
else:
    for ruta in archivos_recortes:
        print(f"\nProcesando: {ruta} ...")
        
        # 1. Preprocesar la imagen antes de pasarla al OCR
        imagen_procesada = preprocesar_imagen(ruta)
        
        # 2. Pasar la imagen procesada (arreglo de numpy) a EasyOCR
        # detail=0 devuelve solo el texto limpio
        resultados = lector.readtext(imagen_procesada, detail=0)
        texto_final = " ".join(resultados)
        
        if texto_final:
            print(f"👉 Resultado: '{texto_final}'")
        else:
            print("👉 Resultado: [La IA no pudo leer nada aquí]")

print("\n¡Lectura finalizada!")