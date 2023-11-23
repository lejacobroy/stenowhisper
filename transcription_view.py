from transcriber import *
from audio_file import *

class TranscriptionView:
    def __init__(self, audio_library):
        self.audio_library = audio_library
        self.transcriber = Transcriber()

    def start(self):
        while True:
            print("1. Upload Audio File")
            print("2. Display Audio Files")
            print("3. Transcribe Audio File")
            print("4. Display Transcription Status")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.upload_audio_file()
            elif choice == "2":
                self.display_audio_files()
            elif choice == "3":
                self.transcribe_audio_file()
            elif choice == "4":
                self.display_transcription_status()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def upload_audio_file(self):
        file_id = input("Enter file ID: ")
        file_name = input("Enter file name: ")
        file_path = input("Enter file path: ")

        audio_file = AudioFile(file_id, file_name, file_path)
        self.audio_library.add_audio_file(audio_file)

        print("Audio file uploaded successfully.")

    def display_audio_files(self):
        audio_files = self.audio_library.get_all_audio_files()

        if not audio_files:
            print("No audio files in the library.")
        else:
            print("Audio Files:")
            for audio_file in audio_files:
                print(f"ID: {audio_file.file_id}, Name: {audio_file.file_name}")

    def transcribe_audio_file(self):
        file_id = input("Enter file ID to transcribe: ")
        audio_file = self.audio_library.get_audio_file(file_id)

        if audio_file:
            self.transcriber.transcribe_audio(audio_file)
            print("Audio file transcribed successfully.")
        else:
            print("Audio file not found.")

    def display_transcription_status(self):
        file_id = input("Enter file ID to check transcription status: ")
        audio_file = self.audio_library.get_audio_file(file_id)

        if audio_file:
            status = self.transcriber.get_transcription_status(audio_file)
            print(f"Transcription Status: {status}")
        else:
            print("Audio file not found.")
