# yt-downloader
# Descargador de videos de YouTube
# Autor: CodingCruz
# Fecha: 2025-08-09
# Versión: 1.0
#
# Python 3.13.5
# tkinter 8.6
# ttkbootstrap 1.10.1
# yt-dlp 2025.08.09


import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SUCCESS, INFO
import yt_dlp
import threading
from queue import Queue

# Función para descargar el video
def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Por favor, ingresa una URL de YouTube.")
        return

    save_path = filedialog.askdirectory(title="Selecciona la carpeta de destino")
    if not save_path:
        return

    audio_only = audio_only_var.get()
    max_quality = max_quality_var.get()

    download_btn.config(state='disabled')
    log_queue.put("Iniciando descarga...\n")

    thread = threading.Thread(target=download_thread, args=(url, save_path, audio_only, max_quality))
    thread.start()

# Función para manejar la descarga en un hilo separado
def download_thread(url, save_path, audio_only, max_quality):
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: progress_hook(d, log_queue)],
        'logger': MyLogger(log_queue),
        'verbose': True,
    }

    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif max_quality:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        log_queue.put("Descarga completada con éxito.\n")
        root.after(0, lambda: messagebox.showinfo("Éxito", "Video descargado correctamente."))
    except Exception as e:
        log_queue.put(f"Error: {str(e)}\n")
        root.after(0, lambda: messagebox.showerror("Error", f"Ocurrió un error: {str(e)}"))
    finally:
        root.after(0, lambda: download_btn.config(state='normal'))

# Clase personalizada para el logger
class MyLogger:
    def __init__(self, queue):
        self.queue = queue

    def debug(self, msg):
        self.queue.put(msg + '\n')

    def info(self, msg):
        self.queue.put(msg + '\n')

    def warning(self, msg):
        self.queue.put(msg + '\n')

    def error(self, msg):
        self.queue.put(msg + '\n')

def progress_hook(d, queue):
    if d['status'] == 'downloading':
        queue.put(f"Descargando: {d['_percent_str']} de {d['_total_bytes_str']} a {d['_speed_str']} ETA {d['_eta_str']}\n")
    elif d['status'] == 'finished':
        queue.put("Descarga completada, procesando...\n")

# Crear la ventana principal
root = ttk.Window(themename="darkly")
root.title("Descargador de YouTube")
root.geometry("500x400")

# Etiqueta y entrada para URL
# Frame para URL
ttk.Label(root, text="URL de YouTube:").pack(pady=10)
url_frame = ttk.Frame(root)
url_frame.pack()
url_entry = ttk.Entry(url_frame, width=40)
url_entry.pack(side=tk.LEFT)
def paste_url():
    try:
        url_entry.insert(0, root.clipboard_get())
    except:
        pass
paste_btn = ttk.Button(url_frame, text="Pegar", bootstyle=INFO, command=paste_url)
paste_btn.pack(side=tk.LEFT, padx=5)

# Opciones en una línea
options_frame = ttk.Frame(root)
options_frame.pack(pady=10)
max_quality_var = tk.BooleanVar()
ttk.Checkbutton(options_frame, text="Máxima calidad", bootstyle=PRIMARY, variable=max_quality_var).pack(side=tk.LEFT, padx=10)
audio_only_var = tk.BooleanVar()
ttk.Checkbutton(options_frame, text="Solo audio (MP3)", bootstyle=PRIMARY, variable=audio_only_var).pack(side=tk.LEFT, padx=10)

# Botón de descarga
download_btn = ttk.Button(root, text="Descargar", bootstyle=SUCCESS, command=download_video)
download_btn.pack(pady=20)

# Cola para logs
log_queue = Queue()

# Frame para el log
log_frame = ttk.Frame(root)
log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
log_text = tk.Text(log_frame, height=10, wrap='word')
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')
log_text.config(yscrollcommand=scrollbar.set)

def process_queue():
    try:
        while not log_queue.empty():
            msg = log_queue.get_nowait()
            log_text.insert(tk.END, msg)
            log_text.see(tk.END)
    except:
        pass
    root.after(100, process_queue)

process_queue()

root.mainloop()