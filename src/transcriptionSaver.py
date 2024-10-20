import json
import csv
import os
from datetime import timedelta

class TranscriptionSaver:
    def __init__(self, result, output_types, output_dir, output_filename='output'):
        self.result = result
        self.segments = result["segments"]
        self.output_types = output_types if output_types != 'all' else ['txt', 'vtt', 'srt', 'tsv', 'json']
        self.output_dir = output_dir
        self.encoding = 'utf-8'
        self.output_filename = output_filename

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self):
        for output_type in self.output_types:
            if output_type == 'txt':
                self._save_txt()
            elif output_type == 'vtt':
                self._save_vtt()
            elif output_type == 'srt':
                self._save_srt()
            elif output_type == 'tsv':
                self._save_tsv()
            elif output_type == 'json':
                self._save_json()

    def _save_txt(self):
        with open(os.path.join(self.output_dir, self.output_filename + ".txt"), "w", encoding=self.encoding) as f:
            f.write(self.result["text"])

    def _save_vtt(self):
        def format_timestamp(seconds):
            delta = timedelta(seconds=seconds)
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = delta.microseconds // 1000
            return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

        with open(os.path.join(self.output_dir, self.output_filename + ".vtt"), "w", encoding=self.encoding) as f:
            f.write("WEBVTT\n\n")
            for segment in self.segments:
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"]
                f.write(f"{start} --> {end}\n{text}\n\n")

    def _save_srt(self):
        def format_timestamp_srt(seconds):
            delta = timedelta(seconds=seconds)
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = delta.microseconds // 1000
            return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

        with open(os.path.join(self.output_dir, self.output_filename + ".srt"), "w", encoding=self.encoding) as f:
            for i, segment in enumerate(self.segments, start=1):
                start = format_timestamp_srt(segment["start"])
                end = format_timestamp_srt(segment["end"])
                text = segment["text"]
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    def _save_tsv(self):
        with open(os.path.join(self.output_dir, self.output_filename + ".tsv"), "w", newline="",encoding=self.encoding) as f:
            tsv_writer = csv.writer(f, delimiter='\t')
            tsv_writer.writerow(["start", "end", "text"])
            for segment in self.segments:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                tsv_writer.writerow([start, end, text])

    def _save_json(self):
        with open(os.path.join(self.output_dir, self.output_filename + ".json"), "w",encoding=self.encoding) as f:
            json.dump(self.result, f, indent=4)

# # Example usage
# if __name__ == "__main__":
#     model = whisper.load_model("base")
#     result = model.transcribe("audio_file_path")

#     output_types = 'all'  # or a list of specific types like ['txt', 'json']
#     output_dir = "./output"

#     saver = TranscriptionSaver(result, output_types, output_dir)
#     saver.save()
