import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutoCommitHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"📄 Arquivo modificado: {event.src_path}")
        try:
            # git add .
            subprocess.run(["git", "add", "."], check=True)

            # git commit
            subprocess.run(["git", "commit", "-m", "auto commit"], check=True)

            # git push
            subprocess.run(["git", "push"], check=True)

            print("✅ Commit + Push automático realizado!\n")

        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar comando: {e}")

if __name__ == "__main__":
    path = "."  # repositório atual
    event_handler = GitAutoCommitHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("👀 Monitorando alterações... Ctrl+C para parar.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
