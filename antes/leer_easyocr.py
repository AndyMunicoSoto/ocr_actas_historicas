import easyocr
import os

print("Descargando modelo EasyOCR en Español (Solo la primera vez)...")
# Iniciamos el lector indicando que queremos leer español ('es')
lector = easyocr.Reader(['es'])

archivos_recortes = [
    "recorte_clase_0.jpg",
    "recorte_clase_1.jpg",
    "recorte_clase_2.jpg"
]

print("\n" + "="*50)
print(" INICIANDO EXTRACCIÓN CON EASY-OCR (ESPAÑOL)")
print("="*50)

for ruta in archivos_recortes:
    if not os.path.exists(ruta):
        continue
        
    print(f"\nProcesando: {ruta}")
    
    # detail=0 nos devuelve solo el texto limpio, sin las coordenadas internas de las letras
    resultados = lector.readtext(ruta, detail=0)
    
    # Unir las palabras encontradas
    texto_final = " ".join(resultados)
    
    if texto_final:
        print(f"👉 Resultado: '{texto_final}'")
    else:
        print("👉 Resultado: [La IA no encontró letras legibles]")

print("\n" + "="*50)