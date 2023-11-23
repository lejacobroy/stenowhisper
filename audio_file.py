class AudioFile:
    def __init__(self, file_id, file_name, file_path):
        self.file_id = file_id
        self.file_name = file_name
        self.file_path = file_path
        self.transcription_status = "Not Transcribed"
        self.transcription_text = ""

    def set_transcription_status(self, status):
        self.transcription_status = status

    def set_transcription_text(self, text):
        self.transcription_text = text
