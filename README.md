# stenowhisper

This is an audio transcription app built with Flask and Python. The app allows users to upload audio files, transcribe them using the OpenAI Whisper ASR local model, and view the transcription status.

## Features

- Upload audio files in various formats.
- Transcribe uploaded audio files using the OpenAI Whisper ASR local model.
- View the transcription status of each audio file.

## Prerequisites

- Python 3.7 or higher

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/lejacobroy/stenowhisper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd stenowhisper
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask development server:

   ```bash
   python main.py
   ```

2. Open your web browser and go to `http://localhost:5000` to access the app.

3. Upload an audio file by clicking on the "Upload" button and selecting the file from your local machine.

4. Once the file is uploaded, you can view the transcription status by clicking on the "Status" button.

5. To transcribe the uploaded audio file, click on the "Transcribe" button.

6. To stop the transcription process, click on the "Stop Transcription" button.

## Folder Structure

The project follows the following folder structure:

```
audio-transcription-app/
  ├── app.py
  ├── audio_file.py
  ├── database.py
  ├── main.py
  ├── models.py
  ├── transcriber.py
  ├── templates/
  │   └── index.html
  └── static/
      └── styles.css
```

- `app.py`: Contains the Flask application routes and logic.
- `audio_file.py`: Defines the `AudioFile` data class for storing audio file information.
- `database.py`: Handles the SQLite database operations for storing and retrieving audio files.
- `main.py`: Entry point of the application.
- `models.py`: Contains the `AudioLibrary` and `TranscriptionView` classes.
- `transcriber.py`: Implements the `Transcriber` class for transcribing audio files using the OpenAI Whisper ASR local model.
- `templates/`: Directory containing HTML templates for the Flask views.
- `static/`: Directory containing static files such as CSS stylesheets.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.