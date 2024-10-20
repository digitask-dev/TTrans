import unittest
from src.transcriptionSaver import TranscriptionSaver
import json
import csv
import os

class TestTranscriptionSaver(unittest.TestCase):

    def setUp(self):
        self.result = {
            "text": "This is a test transcription",
            "segments": [
                {"start": 0, "end": 10, "text": "This is a test"},
                {"start": 10, "end": 20, "text": "transcription"}
            ]
        }
        self.output_types = ['txt', 'vtt', 'srt', 'tsv', 'json']
        self.output_dir = "./output"
        self.output_filename = "test"
        self.saver = TranscriptionSaver(self.result, self.output_types, self.output_dir, self.output_filename)

    def test_init(self):
        self.assertEqual(self.saver.result, self.result)
        self.assertEqual(self.saver.segments, self.result["segments"])
        self.assertEqual(self.saver.output_types, self.output_types)
        self.assertEqual(self.saver.output_dir, self.output_dir)
        self.assertEqual(self.saver.output_filename, self.output_filename)

    def test_save_txt(self):
        self.saver._save_txt()
        with open(os.path.join(self.output_dir, self.output_filename + ".txt"), "r") as f:
            self.assertEqual(f.read(), self.result["text"])
        os.remove(os.path.join(self.output_dir, self.output_filename + ".txt"))

    def test_save_vtt(self):
        self.saver._save_vtt()
        with open(os.path.join(self.output_dir, self.output_filename + ".vtt"), "r") as f:
            vtt_content = f.read()
            self.assertIn("WEBVTT", vtt_content)
            self.assertIn("This is a test", vtt_content)
            self.assertIn("transcription", vtt_content)
        os.remove(os.path.join(self.output_dir, self.output_filename + ".vtt"))

    def test_save_srt(self):
        self.saver._save_srt()
        with open(os.path.join(self.output_dir, self.output_filename + ".srt"), "r") as f:
            srt_content = f.read()
            self.assertIn("1", srt_content)
            self.assertIn("00:00:00,000 --> 00:00:10,000", srt_content)
            self.assertIn("This is a test", srt_content)
            self.assertIn("2", srt_content)
            self.assertIn("00:00:10,000 --> 00:00:20,000", srt_content)
            self.assertIn("transcription", srt_content)
        os.remove(os.path.join(self.output_dir, self.output_filename + ".srt"))

    def test_save_tsv(self):
        self.saver._save_tsv()
        with open(os.path.join(self.output_dir, self.output_filename + ".tsv"), "r") as f:
            tsv_content = f.read()
            self.assertIn("start\tend\ttext", tsv_content)
            self.assertIn("0\t10\tThis is a test", tsv_content)
            self.assertIn("10\t20\ttranscription", tsv_content)
        os.remove(os.path.join(self.output_dir, self.output_filename + ".tsv"))

    def test_save_json(self):
        self.saver._save_json()
        with open(os.path.join(self.output_dir, self.output_filename + ".json"), "r") as f:
            json_content = json.load(f)
            self.assertEqual(json_content, self.result)
        os.remove(os.path.join(self.output_dir, self.output_filename + ".json"))

    def tearDown(self):
        if os.path.exists(self.output_dir):
            os.rmdir(self.output_dir)

if __name__ == '__main__':
    unittest.main()