class AudioLibrary:
    def __init__(self):
        self.audio_files = []

    def add_audio_file(self, audio_file):
        self.audio_files.append(audio_file)

    def get_audio_file(self, file_id):
        for audio_file in self.audio_files:
            if audio_file.file_id == file_id:
                return audio_file
        return None

    def get_all_audio_files(self):
        return self.audio_files
