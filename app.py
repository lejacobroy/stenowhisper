import os
from flask import Flask, render_template, request, jsonify, redirect
from models import AudioFile, AudioLibrary, TranscriptionView
from werkzeug.utils import secure_filename
from pathlib import Path
import subprocess
import sys
import json
ROOT_FOLDER = Path(__file__).parent.absolute()
UPLOAD_FOLDER = 'audiofiles' 

app = Flask(__name__)
audio_library = AudioLibrary()
transcription_view = TranscriptionView(audio_library)

@app.route('/')
def display_files():
    audio_files = audio_library.get_all_audio_files()
    files = []
    if not audio_files:
        return render_template('index.html', files=files)
    else:
        for audio_file in audio_files:
            files.append({
                'id': audio_file.id, 
                'name': audio_file.file_name, 
                'file_path': audio_file.file_path, 
                'transcription_status': audio_file.transcription_status, 
                'transcription_text': audio_file.transcription_text
                })
        return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_file' in request.files:
        file = request.files['audio_file'] 
        filename = secure_filename(file.filename)
        file_path = os.path.join(ROOT_FOLDER, UPLOAD_FOLDER, filename)
        print(ROOT_FOLDER, UPLOAD_FOLDER, file_path)
        file.save(file_path)

        file_name = os.path.splitext(filename)[0]
        print(file_name, file_path)
        audio_file = AudioFile(0, file_name, file_path)
        audio_library.add_audio_file(audio_file)

        files = audio_library.get_all_audio_files()

    return redirect('/file/'+str(files[-1].id))

@app.route('/transcribe', methods=['POST'])
def transcribe():
    id = request.form['file-id']
 
    audio_file = audio_library.get_audio_file(id)

    if audio_file:
        audio_file.transcription_status = 'in progress'
        audio_library.update_audio_file(audio_file)
        #transcription_view.transcribe_audio_file(audio_file)
        subprocess.Popen([sys.executable,  os.path.join(ROOT_FOLDER,'transcription.py'), str(audio_file.id)])

        return redirect('/file/'+str(audio_file.id))
    return redirect('/')

@app.route('/stop_transcription', methods=['POST'])
def stop_transcription():
    id = request.form['id']
    audio_file = audio_library.get_audio_file(id)

    if audio_file:
        transcription_view.stop_transcription(audio_file)
    return redirect('/')

@app.route('/status', methods=['POST'])
def status():
    id = request.form['id']
    audio_file = audio_library.get_audio_file(id)

    if audio_file:
        status = transcription_view.get_transcription_status(audio_file)
    return redirect('/')

# New route for viewing the transcription of a file
@app.route('/file/<int:id>', methods=['GET'])
def view_transcription(id):
    # Retrieve the file data based on the provided id
    # Replace this with your actual data retrieval logic
    audio_file = audio_library.get_audio_file(id)

    if not audio_file:
        return redirect('/')
    else:
        file = {
                'id': audio_file.id, 
                'name': audio_file.file_name, 
                'file_path': audio_file.file_path, 
                'transcription_status': audio_file.transcription_status, 
                'transcription_text': audio_file.transcription_text,
                'transcription_chunks': json.loads(audio_file.transcription_chunks)
                }
        return render_template('file.html', file=file)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)