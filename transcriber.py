from transformers import pipeline
import subprocess
from pathlib import Path
from database import Database
from pydub import AudioSegment

class Transcriber:
    def __init__(self):
        self.database = Database()
        self.database.create_tables()
        # load model and processor
        #processor = WhisperProcessor.from_pretrained("openai/whisper-small")
        #model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
        #forced_decoder_ids = processor.get_decoder_prompt_ids(language="french", task="transcribe")

        self.transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-small")

    def _convert_to_wav(self, audio_file):
        temp_dir = Path("/tmp")
        wav_path = temp_dir / "audio.wav"
        if audio_file.file_path.endswith(".wav"):
            return audio_file.file_path
        
        original = AudioSegment.from_file(audio_file.file_path)
        converted = original.set_frame_rate(16000).set_channels(1)
        converted.export(wav_path, format="wav")

        return str(wav_path)

    def transcribe_audio(self, audio_file):
        # convert to wav file
        wav_file = self._convert_to_wav(audio_file)

        # Transcribe the audio file using the Whisper LLM model
        transcription = self.transcriber(audio_file.file_path, generate_kwargs={"language": "french"})["text"]
        print(transcription)
        # load streaming dataset and read first audio sample
        #ds = audio_file.file_path
        #ds = ds.cast_column("audio", Audio(sampling_rate=16_000))
        #input_speech = next(iter(ds))["audio"]
        #input_features = self.processor(audio_file.file_path, sampling_rate=16_000, return_tensors="pt").input_features

        # generate token ids
        #predicted_ids = self.model.generate(input_features, forced_decoder_ids=self.forced_decoder_ids)
        # decode token ids to text
        #transcription = self.processor.batch_decode(predicted_ids)
        #['<|startoftranscript|><|fr|><|transcribe|><|notimestamps|> Un vrai travail intéressant va enfin être mené sur ce sujet.<|endoftext|>']

        #transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)

        # Update the audio file with the transcription text and status
        self.set_transcription_text(audio_file, transcription)
        self.set_transcription_status(audio_file,"Transcribed")

    def set_transcription_text(self, audio_file, transcription_text):
        audio_file.transcription_text = transcription_text
        self.database.update_audio_file(audio_file)

    def set_transcription_status(self, audio_file, transcription_status):
        audio_file.transcription_status = transcription_status
        self.database.update_audio_file(audio_file)
