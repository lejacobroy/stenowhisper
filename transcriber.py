from transformers import pipeline
import ffmpeg
from pathlib import Path
import os
import json
from database import Database
from pyannote.audio import Pipeline
import re
from pydub import AudioSegment
import webvtt
import pysrt
from dotenv import load_dotenv
from datetime import timedelta
import torch
import numpy as np
#from faster_whisper import WhisperModel
#https://huggingface.co/good-tape/faster-whisper-large-v3
#model = WhisperModel("flyingleafe/faster-whisper-large-v3")
class Transcriber:
    def __init__(self):
        load_dotenv()
        self.database = Database()
        self.database.create_tables()
        self.temp = Path(__file__).parent.absolute()
        self.diar_path = os.path.join(self.temp, 'temp', 'diarization.txt')
        self.wav_path = os.path.join(self.temp, 'temp', 'audio.wav')

        self.annote_pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization-3.1',
                                                        use_auth_token=os.getenv('HF_TOKEN'))
        self.annote_pipeline.to(torch.device("mps"))
        self.transcriber = pipeline("automatic-speech-recognition", 
                                    chunk_length_s=10, 
                                    #stride_length_s=(4,2), 
                                    return_timestamps=True, 
                                    model="openai/whisper-large-v3")


    def convert_to_wav(self, audio_file):
        if audio_file.file_path.endswith(".wav"):
            return audio_file.file_path  
        ffmpeg.input(audio_file.file_path, hide_banner=None, y=None).output(self.wav_path, ar=16000, ac=1, loglevel='error').run(overwrite_output=True)

    def speaker_diarization(self):
        dz = self.annote_pipeline(self.wav_path, num_speakers=2)  
        with open(self.diar_path, "w") as text_file:
            text_file.write(str(dz))

    def millisec(self, timeStr):
        spl = timeStr.split(":")
        s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
        return s

    def read_diarization(self):
        audio = AudioSegment.from_wav(self.wav_path)
        spacermilli = 2000
        spacer = AudioSegment.silent(duration=spacermilli)
        audio = spacer.append(audio, crossfade=0)
        sounds = spacer
        segments = []
        dz = open(self.diar_path).read().splitlines()
        for l in dz:
            start, end =  tuple(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=l))
            start = int(self.millisec(start)) #milliseconds
            end = int(self.millisec(end))  #milliseconds
            audio[start:end].export(os.path.join(self.temp,'temp','dz.wav'), format="wav") #Exports to a wav file in the current path.
            transcription = self.transcriber(
                                                os.path.join(self.temp,'temp','dz.wav'), 
                                                batch_size=8, 
                                                return_timestamps=True, 
                                                generate_kwargs={"language": "french"})
            print(l,transcription['text'])
            segments.append(len(sounds))
            sounds = sounds.append(audio[start:end], crossfade=0)
            sounds = sounds.append(spacer, crossfade=0)

        sounds.export(os.path.join(self.temp,'temp','dz.wav'), format="wav") #Exports to a wav file in the current path.
        print(segments)

        captions = [[(int)(self.millisec(caption.start)), (int)(self.millisec(caption.end)),  caption.text] for caption in webvtt.read(os.path.join(self.temp,'temp','dz.vtt'))]
        print(*captions[:8], sep='\n')

        preS = '\n\n  \n    \n    \n    \n    Lexicap\n    \n  \n  \n    Yann LeCun: Dark Matter of Intelligence and Self-Supervised Learning | Lex Fridman Podcast #258\n  \n    \n'
        postS = '\t\n'

        html = list(preS)

        for i in range(len(segments)):
            idx = 0
            for idx in range(len(captions)):
                if captions[idx][0] >= (segments[i] - spacermilli):
                    break;
        
        while (idx < (len(captions))) and ((i == len(segments) - 1) or (captions[idx][1] < segments[i+1])):
            c = captions[idx]  
            
            start = captions[i][0] + (c[0] -segments[i])

            if start < 0: 
                start = 0
            idx += 1

            start = start / 1000.0
            startStr = '{0:02d}:{1:02d}:{2:02.2f}'.format((int)(start // 3600), 
                                                    (int)(start % 3600 // 60), 
                                                    start % 60)
            
            html.append('\t\t\t\n')
            html.append(f'\t\t\t\tlink |\n')
            html.append(f'\t\t\t\t{startStr}\n')
            html.append(f'\t\t\t\t{"[Lex]" if captions[i][2] else "[Yann]"} {c[2]}\n')
            html.append('\t\t\t\n\n')

        html.append(postS)
        s = "".join(html)

        with open("lexicap.html", "w") as text_file:
            text_file.write(s)
        print(s)

    def save_to_vtt(self, data):
        vtt_content = "WEBVTT\n\n"

        for entry in data:
            start_time = int(entry["timestamp"][0]* 1000)
            end_time = int(entry["timestamp"][1]* 1000)
            text = entry["text"]
            
            vtt_content += f"{start_time:.2f} --> {end_time:.2f}\n{text}\n\n"

        with open(os.path.join(self.temp,'temp','dz.vtt'), "w", encoding="utf-8") as vtt_file:
            vtt_file.write(vtt_content)

        print("Conversion completed. Output saved to 'output.vtt'")

    def transcribe_audio(self, audio_file):
        # convert to wav file
        print('Converting to wav...')
        self.convert_to_wav(audio_file)
        print('Converting to wav... Done')

        print('Running speaker diarization...')
        # Run speaker diarization on the wav file
        self.speaker_diarization()
        print('Running speaker diarization... Done')


        # Transcribe the audio file using the Whisper LLM model
        print('Transcribing audio...')
        transcription = self.transcriber(self.wav_path, batch_size=8, return_timestamps=True, generate_kwargs={"language": "french"})
        print('Transcribing audio... Done')

        print('Saving transcription...')
        self.save_to_vtt(transcription['chunks'])
        print('Saving transcription... Done')

        print('Reading diarization...')
        # Read the diarization file and create a list of segments
        self.read_diarization()
        print('Reading diarization... Done')

        print('Updating audio file...')
        # Update the audio file with the transcription text and status
        self.set_transcription(audio_file, transcription['text'], transcription_status="Transcribed", transcription_chunks=transcription['chunks'])
        print('Updating audio file... Done')

    def set_transcription(self, audio_file, transcription_text, transcription_status, transcription_chunks):
        audio_file.transcription_text = transcription_text
        audio_file.transcription_status = transcription_status
        audio_file.transcription_chunks = json.dumps(transcription_chunks)
        self.database.update_audio_file(audio_file)