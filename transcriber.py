from transformers import pipeline
import ffmpeg
from pathlib import Path
import os
from database import Database


class Transcriber:
    def __init__(self):
        self.database = Database()
        self.database.create_tables()
        # load model and processor
        # processor = WhisperProcessor.from_pretrained("openai/whisper-small")
        # model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
        # forced_decoder_ids = processor.get_decoder_prompt_ids(language="french", task="transcribe")

        self.transcriber = pipeline("automatic-speech-recognition", chunk_length_s=10, stride_length_s=(4,2), return_timestamps=True, model="openai/whisper-medium")

    def _convert_to_wav(self, audio_file):
        temp = Path(__file__).parent.absolute()
        wav_path = os.path.join(temp, 'temp', 'audio.wav')

        if audio_file.file_path.endswith(".wav"):
            return audio_file.file_path
        
        print(audio_file.file_path, wav_path)
        ffmpeg.input(audio_file.file_path, hide_banner=None, y=None).output(wav_path, ar=16000, ac=1, loglevel='error').run(overwrite_output=True)

        return str(wav_path)

    def transcribe_audio(self, audio_file):
        # convert to wav file
        wav_file = self._convert_to_wav(audio_file)

        # Transcribe the audio file using the Whisper LLM model
        transcription = self.transcriber(wav_file, batch_size=8, return_timestamps=True, generate_kwargs={"language": "french"})
        print(transcription)
        # Update the audio file with the transcription text and status
        self.set_transcription_text(audio_file, transcription['text'])
        self.set_transcription_status(audio_file, "Transcribed")

    def set_transcription_text(self, audio_file, transcription_text):
        audio_file.transcription_text = transcription_text
        self.database.update_audio_file(audio_file)

    def set_transcription_status(self, audio_file, transcription_status):
        audio_file.transcription_status = transcription_status
        self.database.update_audio_file(audio_file)