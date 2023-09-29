import os
import random
import string
import time
import psutil
import subprocess
import arquivos as arq
import threading
import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def on_any_event(self, event):
        if event.is_directory:
            return None

        filename = os.path.basename(event.src_path)
        for path in arq.paths.values():
            specified_filename = os.path.basename(path)
            if filename.startswith(specified_filename):
                message = f"{event.event_type.capitalize()} arquivo: {event.src_path}"
                self.log_event(message)
                self.update_gui(message)
                matar()

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(arq.log.log_file_path, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"Logged event: [{timestamp}] {message}")

    def update_gui(self, message):
        print(f"Updating GUI with message: {message}")
        self.text_widget.after(0, self.text_widget.insert, tk.END, message + '\n')

class ObserverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Eventos")

        self.text_widget = tk.Text(root, wrap=tk.WORD, height=10, width=40)
        self.text_widget.pack()

        self.start_button = tk.Button(root, text="Iniciar Monitor", command=self.start_observer)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Parar Monitoramento", command=self.stop_observer)
        self.stop_button.pack()

        self.observer = None

    def start_observer(self):
        def target():
            event_handler = MyHandler(self.text_widget)
            self.observer = Observer()
            for path in arq.paths.values():
                if os.path.exists(path):
                    print(f"Agendando observador para o caminho: {path}")  # Adicionado
                    self.observer.schedule(event_handler, path, recursive=False)
                else:
                    print(f"O diretório {path} não existe.")
            
            # Cria honeypots na pasta de documentos
            self.create_honeypots()  # Modificado aqui

            print("Iniciando observador...")
            self.observer.start()
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.observer.stop        
            self.observer.join()

        threading.Thread(target=target).start()

    def stop_observer(self):
        if self.observer:
            print("Parando observador...")  # Adicionado
            self.observer.stop()
            
            # Exclui os honeypots da pasta de documentos
            self.delete_honeypots()  # Modificado aqui

    def create_random_file(self):
        filename = ''.join(random.choices(string.ascii_lowercase, k=10)) + '.txt'
        filepath = os.path.join(arq.paths['documents'], filename)
        with open(filepath, 'w') as f:
            f.write('Este é um arquivo honeypot.')

    def create_honeypots(self):
        num_honeypots = 5  # Quantidade de honeypots a serem criados
        for _ in range(num_honeypots):
            self.create_random_file()

    def delete_honeypots(self):
        for filename in os.listdir(arq.documents_path):
            filepath = os.path.join(arq.documents_path, filename)
            if os.path.isfile(filepath) and filename.endswith('.txt'):
                os.remove(filepath)

def is_legitimate(process):
    try:
        exe_path = process.info['exe']
        if exe_path != None and not exe_path.startswith("C:\\Windows") and process.info['name'] not in ["System", "Registry", "python.exe", "Catcher.exe", "Catcher.py", "arquivos.py", "functions.py"]:
            # exe_path é None ou uma string vazia e não está localizado na pasta "C:\Windows"
            return False
        return True
    except Exception as e:
        print("Erro não previsto:", e)
        return False

def taskkill(pid):
    try:
        subprocess.call(["taskkill", "/F", "/PID", str(pid)])
    except Exception as e:
        print(f"Erro ao tentar matar o processo {pid}: {e}")

def matar():
    proc_mal_pids = set()
    try: 
        for process in psutil.process_iter(["name", "pid", "exe"]):
            legit = is_legitimate(process)
            if not legit:
                proc_mal_pids.add(process.pid)
            else:
                continue
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    for proc in proc_mal_pids:
        print(proc)
        taskkill(proc)