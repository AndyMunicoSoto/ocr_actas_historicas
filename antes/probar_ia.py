from ultralytics import YOLO

# 1. Cargar TU modelo entrenado (el "cerebro" que acabas de crear)
# Asegúrate de que la ruta coincida con la que se creó en tu carpeta
ruta_modelo = "runs/detect/actas_v1/weights/best.pt"
modelo_ia = YOLO(ruta_modelo)

# 2. La imagen que queremos que la IA analice (como si llegara un acta nueva)
#imagen_prueba = "acta_belaunde_limpia.jpg"
imagen_prueba = "dataset_actas/train/images/acta_belaunde_limpia.jpg"
print(f"Pasando el documento '{imagen_prueba}' por la IA...")

# 3. Hacer la predicción (Inferencia)
resultados = modelo_ia.predict(
    source=imagen_prueba,
    conf=0.10,  # Le pedimos que solo dibuje la caja si está 50% segura o más
    save=True   # ¡Clave! Esto le dice a YOLO que guarde una copia de la foto con las cajas pintadas
)

print("\n¡Análisis completado! La IA ha creado una nueva carpeta.")
print("Ve a 'runs/detect/predict/' y abre la imagen que está adentro.")