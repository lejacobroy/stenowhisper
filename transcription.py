from models import AudioFile, AudioLibrary, TranscriptionView
import sys


def transcribe_audio_file():
    # Access the command-line arguments using sys.argv
    if len(sys.argv) > 1:
        audio_file_id = sys.argv[1]
        audio_library = AudioLibrary()
        transcription_view = TranscriptionView(audio_library)
        audio_file = audio_library.get_audio_file(int(audio_file_id))

        print(f"Transcribing audio file with ID: {audio_file.id}")

        transcription_view.transcribe_audio_file(audio_file)
        
        # Your transcription logic using the audio_file_id
    else:
        print("No audio file ID provided.")
if __name__ == '__main__':
    transcribe_audio_file()