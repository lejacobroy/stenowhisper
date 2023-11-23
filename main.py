from audio_library import AudioLibrary
from transcription_view import TranscriptionView

# Create instances of AudioLibrary and TranscriptionView
audio_library = AudioLibrary()
transcription_view = TranscriptionView(audio_library)

# Start the application
transcription_view.start()
