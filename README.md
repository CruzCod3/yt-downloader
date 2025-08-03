# yt-downloader

Una aplicación de escritorio sencilla para descargar videos de YouTube, con opciones para descargar solo audio o la máxima calidad disponible.

## Características

*   Pega URLs de YouTube directamente.
*   Selecciona la carpeta de destino para las descargas.
*   Opción para descargar solo el audio (convierte a MP3).
*   Opción para descargar el video en la máxima calidad disponible.
*   Log de descarga para ver el progreso y los mensajes.
*   Notificación al completar la descarga con opción para abrir la carpeta.
*   Interfaz limpia y fácil de usar con tema oscuro.

## Requisitos Previos

Asegúrate de tener Python 3 instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/).

Adicionalmente, esta aplicación utiliza FFmpeg para la conversión de audio. Debes tener FFmpeg instalado y accesible en el PATH de tu sistema. Puedes descargarlo desde [ffmpeg.org](https://ffmpeg.org/download.html).

## Instalación

1.  Clona este repositorio o descarga los archivos.
2.  Navega al directorio del proyecto en tu terminal.
3.  Crea un entorno virtual (recomendado):
    ```bash
    python -m venv venv
    ```
    Activa el entorno virtual:
    *   En Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   En macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
4.  Instala las librerías necesarias ejecutando el siguiente comando:
    ```bash
    pip install ttkbootstrap yt-dlp pyperclip
    ```

## Uso

Una vez que hayas instalado las dependencias, puedes ejecutar la aplicación con el siguiente comando:

```bash
python main.py
```
