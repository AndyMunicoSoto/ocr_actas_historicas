from ultralytics import YOLO

# 1. Cargar el modelo base pre-entrenado
# Usamos 'yolov8n.pt' (Nano). Es el más ligero y rápido, ideal para probar en tu computadora sin GPU.
modelo = YOLO('yolov8n.pt') 

if __name__ == '__main__':
    print("Iniciando el entrenamiento de la IA...")
    # 2. Iniciar el entrenamiento (Fine-Tuning)
    resultados = modelo.train(
        data='data.yaml',     # Tu archivo de configuración con las rutas
        epochs=100,            # Cuántas veces va a estudiar tu acta (Épocas)
        imgsz=800,            # Tamaño de imagen que usará internamente
        name='actas_v1',       # Nombre de la carpeta donde guardará su "cerebro" terminado
        augment=False,         # Le damos permiso para hacer trucos de magia (aumentación de datos)
    )
    print("¡Entrenamiento finalizado con éxito!")