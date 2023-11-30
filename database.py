import sqlite3
from pathlib import Path
from dataclasses import dataclass
db_path = Path(__file__).parent.joinpath('database.db').absolute()

@dataclass
class AudioFile:
    id: int
    file_name: str
    file_path: str
    recorded_date: str = ""
    court_session: str = ""
    lawyers: str = ""
    language: str = ""
    transcription_status: str = "Not Transcribed"
    transcription_text: str = ""
    transcription_chunks: str = ""

class Database:
    def create_tables(self):
        self.connection = sqlite3.connect(db_path)
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audio_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT,
                    file_path TEXT,
                    recorded_date TEXT,
                    court_session TEXT,
                    lawyers TEXT,
                    language TEXT,
                    transcription_status TEXT,
                    transcription_text TEXT,
                    transcription_chunks TEXT
                )
            ''')
            self.connection.commit()
            self.connection.close() 

    def insert_audio_file(self, audio_file):
        print(audio_file.file_name, audio_file.file_path)
        self.connection = sqlite3.connect(db_path)
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO audio_files (
                    file_name, file_path
                ) VALUES ( ?, ?)
            ''', (
                audio_file.file_name,
                audio_file.file_path
            ))
            self.connection.commit()
            self.connection.close() 

    def get_audio_file(self, id):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM audio_files WHERE id = ?
            ''', (id,))
            row = cursor.fetchone()
            if row:
                audio_file = AudioFile(
                   id= row['id'],
                   file_name= row['file_name'],
                   file_path= row['file_path'],
                   recorded_date= row['recorded_date'],
                    court_session = row['court_session'],
                    lawyers= row['lawyers'],
                    language = row['language'],
                    transcription_status = row['transcription_status'],
                    transcription_text = row['transcription_text'],
                    transcription_chunks = row['transcription_chunks']
                )
                self.connection.close() 
                return audio_file
        return None

    def get_all_audio_files(self):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM audio_files
            ''')
            rows = cursor.fetchall()
            audio_files = []
            for row in rows:
                audio_file = AudioFile(
                    id= row['id'],
                   file_name= row['file_name'],
                   file_path= row['file_path'],
                   recorded_date= row['recorded_date'],
                    court_session = row['court_session'],
                    lawyers= row['lawyers'],
                    language = row['language'],
                    transcription_status = row['transcription_status'],
                    transcription_text = row['transcription_text'],
                    transcription_chunks = row['transcription_chunks']
                )
                audio_files.append(audio_file)
                self.connection.close() 
            return audio_files
        return []

    def update_audio_file(self, audio_file):
        self.connection = sqlite3.connect(db_path)
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE audio_files SET
                recorded_date = ?,
                court_session = ?,
                lawyers = ?,
                language = ?,
                transcription_status = ?,
                transcription_text = ?,
                transcription_chunks = ?
                WHERE id = ?
            ''', (
                audio_file.recorded_date,
                audio_file.court_session,
                audio_file.lawyers,
                audio_file.language,
                audio_file.transcription_status,
                audio_file.transcription_text,
                audio_file.transcription_chunks,
                audio_file.id
            ))
            self.connection.commit()
            self.connection.close() 