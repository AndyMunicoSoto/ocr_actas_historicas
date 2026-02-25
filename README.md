# 📜 OCR para Actas Históricas (Piloto)

Este proyecto es una prueba de concepto (Pipeline de Inteligencia Artificial) diseñada para automatizar la digitalización y lectura de actas históricas manuscritas, enfocado en caligrafía cursiva antigua.

## 🏗️ Arquitectura del Sistema
El pipeline funciona 100% offline (on-premise) y consta de 4 etapas:
1. **Preprocesamiento:** Limpieza de imagen y mejora de contraste con `OpenCV`.
2. **Detección de Campos (Object Detection):** Modelo personalizado entrenado en `YOLOv8` para identificar cajas delimitadoras (Nombres, Fechas, Firmas).
3. **Recorte Automático:** Script en Python para aislar los campos clave.
4. **Reconocimiento de Texto (HTR/OCR):** Implementación de `TrOCR` (Microsoft) con Fine-Tuning específico para caligrafía en español.

## ⚙️ Tecnologías Utilizadas
* Python 3
* PyTorch & Hugging Face Transformers
* Ultralytics (YOLO)
* OpenCV & Pandas

## 📚 Créditos de Datos
## 📚 Origen de los Datos y Créditos
Para el entrenamiento de transferencia (Fine-Tuning) del modelo de lectura, este proyecto utiliza un corpus de caligrafía histórica peruana. El crédito por los datos corresponde a:

* **Fuente Original:** [Memoria Manuscrita](https://memoriamanuscrita.bnp.gob.pe/), plataforma oficial de la **Biblioteca Nacional del Perú (BNP)**, que custodia, digitaliza y transcribe este invaluable patrimonio histórico.
* **Estructuración del Dataset:** Al repositorio [dataset-phi](https://github.com/gustvjor2005/dataset-phi) (creado por *gustvjor2005*), quien recopiló y formateó las imágenes y etiquetas originales de la BNP para facilitar su uso en arquitecturas de Machine Learning.