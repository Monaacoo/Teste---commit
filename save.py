import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class GitAutoCommitHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        # Ignora arquivos dentro da pasta .git
        if ".git" in event.src_path:
            return

        print(f"📄 Arquivo modificado: {event.src_path}")
        try:
            subprocess.run(["git", "add", "."], check=True)

            # git commit só se houver mudanças
            commit = subprocess.run(
                ["git", "commit", "-m", "auto commit"],
                capture_output=True,
                text=True
            )
            if commit.returncode == 0:
                subprocess.run(["git", "push"], check=True)
                print("✅ Commit + Push automático realizado!\n")
            else:
                print("⚠️ Nada para commitar.")

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
