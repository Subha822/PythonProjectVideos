import os
import whisper
import moviepy as mp
import json

model = whisper.load_model("tiny")

AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac']
VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.avi', '.mov']

def process_media(file_path):
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in AUDIO_EXTENSIONS:
            print(f"Processing audio file: {file_path}")
            result = model.transcribe(file_path)
        elif file_extension in VIDEO_EXTENSIONS:
            print(f"Processing video file: {file_path}")
            video = mp.VideoFileClip(file_path)
            audio_path = "temp_audio.wav"
            video.audio.write_audiofile(audio_path)
            result = model.transcribe(audio_path)
            os.remove(audio_path)
        else:
            print(f"Skipping unsupported file: {file_path}")
            return None
        transcription = result['text']
        save_transcription(file_path, transcription)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def save_transcription(file_path, transcription):
    try:
        output_dir = "transcriptions"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.txt")
        with open(output_path, "w") as f:
            f.write(transcription)
        print(f"Transcription saved for {file_path} at {output_path}")
    except Exception as e:
        print(f"Error saving transcription for {file_path}: {e}")

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_media(file_path)

if __name__ == "__main__":
    folder_to_process = "/workspaces/PythonProjectVideo/Content" 
    process_folder(folder_to_process)
