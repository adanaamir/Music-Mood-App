import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(('.py', '.kv')):
            print("File changed, restarting app...")
            process.kill()
            time.sleep(1)
            start_app()

def start_app():
    global process
    # Pass the --dev flag so main.py knows to skip to dev screen
    process = subprocess.Popen(['python', 'app.py', '--dev'])


if __name__ == "__main__":
    start_app()
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
