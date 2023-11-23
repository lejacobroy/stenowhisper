from transformers import pipeline

class Transcriber:
    def __init__(self):
        # load model and processor
        #processor = WhisperProcessor.from_pretrained("openai/whisper-small")
        #model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
        #forced_decoder_ids = processor.get_decoder_prompt_ids(language="french", task="transcribe")

        self.transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-small")

    def transcribe_audio(self, audio_file):
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
        audio_file.set_transcription_text(transcription)
        audio_file.set_transcription_status("Transcribed")

    def get_transcription_status(self, audio_file):
        return audio_file.transcription_status
