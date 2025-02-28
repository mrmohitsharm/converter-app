import os
import time
import whisper
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Specify directory to monitor
WATCHED_DIR = "./media_files"
SUPPORTED_FORMATS = (".mp3", ".wav", ".mp4", ".mkv", ".mov", ".flv", ".aac", ".m4a")
PROCESSED_FILES = set()

# Load Whisper model
model = whisper.load_model("base")

class TranscriptionHandler(FileSystemEventHandler):
    def process_file(self, file_path):
        if file_path in PROCESSED_FILES:
            return
        
        print(f"Processing: {file_path}")
        transcript_file = file_path + ".txt"
        
        # Load audio properly
        try:
            audio = whisper.load_audio(r"C:\New folder (3)\MedalTVValorant20240627120607.mp4")
            result = model.transcribe(audio)
            
            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            PROCESSED_FILES.add(file_path)
            print(f"Transcription saved: {transcript_file}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def on_created(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith(SUPPORTED_FORMATS):
            threading.Thread(target=self.process_file, args=(event.src_path,)).start()

# Function to scan existing files
def scan_existing_files():
    for root, _, files in os.walk(WATCHED_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(SUPPORTED_FORMATS):
                TranscriptionHandler().process_file(file_path)

# Start monitoring
if __name__ == "__main__":
    if not os.path.exists(WATCHED_DIR):
        os.makedirs(WATCHED_DIR)
    
    print("Scanning existing files...")
    scan_existing_files()
    
    print(f"Monitoring directory: {WATCHED_DIR}")
    event_handler = TranscriptionHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_DIR, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
