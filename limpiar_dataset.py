import csv
import os

# Archivos de entrada y salida
archivo_entrada = 'words/train/gt/words.txt'
archivo_salida = 'words/train/gt/words_1.csv'

print(f"Iniciando limpieza del dataset histórico...")

# Lista para guardar nuestros datos procesados
datos_procesados = []

# Verificar que el archivo exista
if not os.path.exists(archivo_entrada):
    print(f"Error: Crea un archivo llamado '{archivo_entrada}' y pega ahí las etiquetas del dataset.")
else:
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    for linea in lineas:
        # 1. Limpiar saltos de línea de los extremos
        linea = linea.strip()
        
        # Ignorar líneas vacías o encabezados que no sean datos
        if not linea or "Id -- Text" in linea:
            continue
            
        # 2. Estandarizar la separación (algunos tienen "--", otros solo espacio)
        # Reemplazamos el "--" por un espacio vacío para que todo quede uniforme
        linea = linea.replace("--", "").strip()
        
        # 3. Separar el ID de la imagen del texto crudo (cortamos solo en el primer espacio)
        partes = linea.split(" ", 1)
        
        if len(partes) == 2:
            id_imagen = partes[0].strip()
            texto_crudo = partes[1].strip()
            
            # 4. LA MAGIA: Eliminar los separadores de tubería (|)
            texto_limpio = texto_crudo.replace("|", "")
            
            # Al quitar los "|", los espacios originales ("| |") se vuelven espacios normales.
            # Usamos split() y join() para asegurarnos de que no queden dobles espacios por accidente.
            texto_limpio = " ".join(texto_limpio.split())
            
            # 5. Guardamos el ID agregándole ".jpg" para que coincida con las fotos
            nombre_archivo = f"{id_imagen}.png"
            datos_procesados.append([nombre_archivo, texto_limpio])

    # Guardar todo en un CSV súper ordenado
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as f_csv:
        escritor = csv.writer(f_csv)
        escritor.writerow(['filename', 'text']) # Encabezados estándar para Machine Learning
        escritor.writerows(datos_procesados)

    print(f"✅ ¡Éxito! Se procesaron {len(datos_procesados)} etiquetas.")
    print(f"Revisa el archivo '{archivo_salida}' para ver el resultado.")