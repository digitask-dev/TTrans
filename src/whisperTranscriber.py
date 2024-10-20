import os
import whisper
from whisper import tokenizer
import soundfile as sf
import numpy as np
import ffmpeg

class WhisperTranscriber:
    def __init__(self, model_type='base', spoken_language=None):
        self.model_type = model_type
        self.spoken_language = spoken_language
        self.model = whisper.load_model(model_type)

    @staticmethod
    def get_languages():
        languages = tokenizer.LANGUAGES
        # for item in languages:
        #     print(f"{item}, {languages[item]}")
        return list(languages.values())

    @staticmethod
    def get_models():
        return ['base', 'small', 'medium', 'large']

    def transcribe(self, file):
        if self.spoken_language:
            result = self.model.transcribe(file, language=self.spoken_language)
        else:
            result = self.model.transcribe(file)
        return result
    
    def transcribe_with_progress(self, file, progress_callback, result_callback, chunk_size_seconds=30):
        # Load the full audio file
        audio, sample_rate = self.read_audio(file)
        
        # Calculate the total duration of the audio in seconds
        total_duration = len(audio) / sample_rate

        # Calculate the number of chunks
        chunk_size_samples = chunk_size_seconds * sample_rate
        num_chunks = int(np.ceil(len(audio) / chunk_size_samples))

        # Initialize the full transcription result
        full_transcription = {
            "text": "",
            "segments": [],
            "language": None
        }

        # Process each chunk
        for i in range(num_chunks):
            start_sample = i * chunk_size_samples
            end_sample = min((i + 1) * chunk_size_samples, len(audio))
            chunk_audio = audio[start_sample:end_sample]

            # Transcribe the current chunk
            chunk_result = self.model.transcribe(chunk_audio)

            # Append the text
            full_transcription["text"] += chunk_result["text"] + " "

            # Append the segments
            if "segments" in chunk_result:
                for segment in chunk_result["segments"]:
                    # Adjust the segment start and end times based on chunk position
                    segment["start"] += (i * chunk_size_seconds)
                    segment["end"] += (i * chunk_size_seconds)
                    full_transcription["segments"].append(segment)

            # Set the language (assuming it doesn't change across chunks)
            if full_transcription["language"] is None and "language" in chunk_result:
                full_transcription["language"] = chunk_result["language"]

            # Update progress bar
            progress_callback(i + 1, num_chunks)

        # Strip any extra whitespace from the concatenated text
        full_transcription["text"] = full_transcription["text"].strip()

        # Delete the temporary audio file
        self.delete_temp_audio()
        
        # Call the result callback with the full transcription
        result_callback(full_transcription)

    def read_audio(self, file_path, target_sample_rate=16000):
        # Temporary path for the extracted and resampled audio
        temp_audio_path = "temp_audio.wav"

        # Use ffmpeg to extract audio and resample it to the target sample rate
        ffmpeg.input(file_path).output(
            temp_audio_path,
            ar=target_sample_rate,  # Set the audio sample rate
            ac=1,  # Set the number of audio channels to 1 (mono)
            format='wav'  # Output format
        ).run(overwrite_output=True)

        # Read the resampled audio file
        audio_data, sample_rate = sf.read(temp_audio_path)
        
        return audio_data.astype(np.float32), sample_rate

    def delete_temp_audio(self):
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
            
    def set_model(self, model_type):
        self.model_type = model_type
        self.model = whisper.load_model(model_type)

    def set_language(self, spoken_language):
        self.spoken_language = spoken_language

def progress(bit,total):
    print(bit,total)

def result_process(result):
    print(result)
