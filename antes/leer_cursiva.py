import easyocr
import glob
import os

print("Cargando el motor de EasyOCR en Español...")
# Iniciar el lector en español ('es')
lector = easyocr.Reader(['es'])

# Buscar las imágenes recortadas
archivos_recortes = ['imprenta.jpeg']

print("\n" + "="*50)
print(" INICIANDO EXTRACCIÓN CON EASY-OCR")
print(f" Imágenes encontradas: {len(archivos_recortes)}")
print("="*50)

if len(archivos_recortes) == 0:
    print("❌ No se encontraron recortes.")
else:
    for ruta in archivos_recortes:
        print(f"\nProcesando: {ruta} ...")
        
        # detail=0 devuelve solo el texto limpio
        resultados = lector.readtext(ruta, detail=0)
        texto_final = " ".join(resultados)
        
        if texto_final:
            print(f"👉 Resultado: '{texto_final}'")
        else:
            print("👉 Resultado: [La IA no pudo leer nada aquí]")

print("\n¡Lectura finalizada!")