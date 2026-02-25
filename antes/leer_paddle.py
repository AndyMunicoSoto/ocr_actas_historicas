from paddleocr import PaddleOCR
import os

print("Descargando modelo PaddleOCR en Español (Solo la primera vez)...")
# Iniciamos el motor indicando idioma español ('es')
# use_angle_cls=True le ayuda si el texto está un poquito chueco
ocr = PaddleOCR(use_angle_cls=True, lang='es')

archivos_recortes = [
    "recorte_clase_0.jpg",
    "recorte_clase_1.jpg",
    "recorte_clase_2.jpg"
]

print("\n" + "="*50)
print(" INICIANDO EXTRACCIÓN CON PADDLE-OCR (ESPAÑOL)")
print("="*50)

for ruta in archivos_recortes:
    if not os.path.exists(ruta):
        continue
        
    print(f"\nProcesando: {ruta}")
    
    # La IA hace el trabajo sucio aquí
    resultados = ocr.ocr(ruta, cls=True)
    
    # Extraer y mostrar el texto
    if resultados and resultados[0]:
        for linea in resultados[0]:
            # linea[1][0] contiene el texto adivinado
            # linea[1][1] contiene el porcentaje de seguridad (0.0 a 1.0)
            texto = linea[1][0]
            confianza = linea[1][1]
            print(f"👉 Resultado: '{texto}' (Seguridad: {confianza*100:.1f}%)")
    else:
        print("👉 Resultado: [La IA no pudo encontrar letras legibles aquí]")

print("\n" + "="*50)