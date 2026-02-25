import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from transformers import TrOCRProcessor
import os

print("Iniciando la cinta transportadora de datos...")

# 1. Definimos nuestra clase Dataset personalizada
class HistoricalDataset(Dataset):
    def __init__(self, ruta_csv, ruta_imagenes, processor, max_target_length=128):
        # Leemos el CSV usando pandas
        self.df = pd.read_csv(ruta_csv)
        self.ruta_imagenes = ruta_imagenes
        self.processor = processor
        self.max_target_length = max_target_length

    # PyTorch necesita saber cuántas imágenes tenemos en total
    def __len__(self):
        return len(self.df)

    # Aquí ocurre la magia: PyTorch nos pide la imagen número 'idx'
    # Aquí ocurre la magia: PyTorch nos pide la imagen número 'idx'
    def __getitem__(self, idx):
        # Sacamos el nombre del archivo y el texto de esa fila (Ej: "91-P001-L003-W001.jpg")
        nombre_archivo = self.df.iloc[idx]['filename']
        texto_real = self.df.iloc[idx]['text']

        # --- NUEVA LÓGICA DE RUTAS ANIDADAS ---
        # Extraemos el prefijo antes del primer guion (ej. de "91-P..." saca "91")
        subcarpeta = nombre_archivo.split('-')[0]
        
        # Construimos la ruta exacta: ruta_imagenes / 91 / 91-P001-L003-W001.jpg
        ruta_completa = os.path.join(self.ruta_imagenes, subcarpeta, nombre_archivo)
        # --------------------------------------

        # Abrimos la imagen
        try:
            imagen = Image.open(ruta_completa).convert("RGB")
        except Exception as e:
            print(f"⚠️ Error cargando la imagen {ruta_completa}: {e}")
            # Si una imagen falla o no existe, creamos una blanca para no tumbar el entrenamiento
            imagen = Image.new('RGB', (384, 384), color='white')
            texto_real = ""

        # Convertimos la IMAGEN a tensores matemáticos
        pixel_values = self.processor(imagen, return_tensors="pt").pixel_values.squeeze()

        # Convertimos el TEXTO a números (labels)
        labels = self.processor.tokenizer(
            texto_real,
            padding="max_length",
            max_length=self.max_target_length,
            truncation=True
        ).input_ids

        # Reemplazamos el token de relleno por -100
        labels = [label if label != self.processor.tokenizer.pad_token_id else -100 for label in labels]

        return {"pixel_values": pixel_values, "labels": torch.tensor(labels)}
    
'''
# ==========================================
# PRUEBA DE LA CINTA TRANSPORTADORA
# ==========================================
if __name__ == "__main__":
    # Cargamos el procesador del modelo en español que ya descargaste antes
    print("Cargando el procesador TrOCR...")
    processor = TrOCRProcessor.from_pretrained('qantev/trocr-base-spanish')

    # Instanciamos nuestra clase (¡Ajusta la ruta de la carpeta de imágenes si es distinta!)
    # Asumimos que las imágenes están en una carpeta llamada 'imagenes_historicas'
    carpeta_imagenes = "words/train/img" # Cambia esto por el nombre de tu carpeta
    
    if not os.path.exists(carpeta_imagenes):
        print(f"\n ERROR: Crea una carpeta llamada '{carpeta_imagenes}', mete ahí las imágenes del dataset y vuelve a ejecutar.")
    else:
        dataset_entrenamiento = HistoricalDataset(
            ruta_csv='words/train/gt/words_1.csv',
            ruta_imagenes=carpeta_imagenes,
            processor=processor
        )

        print(f"\n✅ Dataset cargado exitosamente. Total de muestras: {len(dataset_entrenamiento)}")
        
        # PyTorch DataLoader agrupa las imágenes en "lotes" (batches) para procesarlas más rápido
        # batch_size=2 significa que le pasará de 2 en 2 a la tarjeta de video
        dataloader = DataLoader(dataset_entrenamiento, batch_size=2, shuffle=True)

        # Probamos sacar el primer lote de la cinta transportadora
        lote_prueba = next(iter(dataloader))
        
        print("\nPrueba del primer Batch:")
        print(f"👉 Forma de los tensores de imagen: {lote_prueba['pixel_values'].shape}")
        print(f"👉 Forma de los tensores de texto: {lote_prueba['labels'].shape}")
        print("\n¡La cinta transportadora está lista para conectar al motor de entrenamiento!")
'''

# ==========================================
# EL MOTOR DE ENTRENAMIENTO (FINE-TUNING)
# ==========================================
if __name__ == "__main__":
    from transformers import VisionEncoderDecoderModel
    import torch.optim as optim

    print("1. Cargando el Procesador y el Modelo base en Español...")

    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

    # --- EL PARCHE: CONFIGURACIÓN DE TOKENS ESPECIALES ---
    model.config.decoder_start_token_id = processor.tokenizer.cls_token_id
    model.config.pad_token_id = processor.tokenizer.pad_token_id
    model.config.vocab_size = model.config.decoder.vocab_size
    # -----------------------------------------------------

    

    #processor = TrOCRProcessor.from_pretrained('qantev/trocr-base-spanish')
    #model = VisionEncoderDecoderModel.from_pretrained('qantev/trocr-base-spanish')

    # Detectar si tienes tarjeta de video (GPU) o si usaremos el procesador (CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"Usando dispositivo: {device.type.upper()}")

    print("\n2. Preparando la cinta transportadora de datos...")
    carpeta_imagenes = "words/train/img" # Asegúrate de que esta ruta sea la correcta
    
    dataset_entrenamiento = HistoricalDataset(
        ruta_csv='words/train/gt/words_1.csv',
        ruta_imagenes=carpeta_imagenes,
        processor=processor
    )
    
    # batch_size=2 para no saturar la memoria RAM de tu computadora
    dataloader = DataLoader(dataset_entrenamiento, batch_size=2, shuffle=True)

    print("\n3. Configurando el Optimizador (El profesor que corrige a la IA)...")
    # AdamW es el estándar de la industria para modelos Transformer
    optimizer = optim.AdamW(model.parameters(), lr=5e-5)

    print("\n" + "="*50)
    print(" INICIANDO EL ENTRENAMIENTO")
    print("="*50)

    # Épocas (Epochs): Cuántas veces la IA leerá el dataset completo
    num_epochs = 3 
    
    model.train() # Ponemos el modelo en modo "aprendizaje"

    for epoch in range(num_epochs):
        print(f"\n--- Iniciando Época {epoch + 1} de {num_epochs} ---")
        
        # Recorremos cada lote de 2 imágenes de la cinta transportadora
        for step, batch in enumerate(dataloader):
            # Movemos los datos a la memoria de la tarjeta de video (o CPU)
            pixel_values = batch["pixel_values"].to(device)
            labels = batch["labels"].to(device)

            # 1. Pase hacia adelante (La IA intenta adivinar)
            outputs = model(pixel_values=pixel_values, labels=labels)
            
            # 2. Calculamos el error (Loss)
            loss = outputs.loss

            # 3. Pase hacia atrás (La IA aprende de su error)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad() # Limpiamos la memoria para la siguiente vuelta

            # Imprimimos el progreso cada 10 pasos
            if step % 10 == 0:
                print(f"Época {epoch + 1} | Paso {step}/{len(dataloader)} | Error (Loss): {loss.item():.4f}")

    print("\n✅ ¡Entrenamiento completado!")
    
    # Guardamos el nuevo cerebro re-entrenado en tu computadora
    carpeta_guardado = "./mi_modelo_historico"
    model.save_pretrained(carpeta_guardado)
    processor.save_pretrained(carpeta_guardado)
    print(f"📁 Tu nuevo modelo especializado se guardó en: {carpeta_guardado}")