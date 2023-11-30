from transcriber import Transcriber
from database import Database

class AudioFile:
    def __init__(self, id, file_name, file_path):
        self.id = id
        self.file_name = file_name
        self.file_path = file_path

class AudioLibrary:
    def __init__(self):
        self.database = Database()
        self.database.create_tables()

    def add_audio_file(self, audio_file):
        print(audio_file.file_name, audio_file.file_path)
        self.database.insert_audio_file(audio_file)
    def update_audio_file(self, audio_file):
        self.database.update_audio_file(audio_file)
    def get_audio_file(self, id):
        return self.database.get_audio_file(id)

    def get_all_audio_files(self):
        return self.database.get_all_audio_files()

class TranscriptionView:
    def __init__(self, audio_library):
        self.audio_library = audio_library
        self.transcriber = Transcriber()

    def transcribe_audio_file(self, audio_file):
        self.transcriber.transcribe_audio(audio_file)
        self.audio_library.database.update_audio_file(audio_file)

    def get_transcription_status(self, audio_file):
        return self.audio_library.database.get_audio_file(audio_file.id).transcription_status
