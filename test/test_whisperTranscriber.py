import unittest
from src.whisperTranscriber import WhisperTranscriber

class TestWhisperTranscriber(unittest.TestCase):
    def setUp(self):
        self.wTranscriber = WhisperTranscriber()

    def test_get_languages(self):
        languages = self.wTranscriber.get_languages()
        self.assertIsInstance(languages, list)
        self.assertGreater(len(languages), 0)

    def test_get_models(self):
        models = self.wTranscriber.get_models()
        self.assertIsInstance(models, list)
        self.assertGreater(len(models), 0)

    def test_set_model(self):
        model_type = 'base'
        self.wTranscriber.set_model(model_type)
        self.assertEqual(self.wTranscriber.model_type, model_type)

    def test_set_language(self):
        language = 'English'
        self.wTranscriber.set_language(language)
        self.assertEqual(self.wTranscriber.spoken_language, language)

if __name__ == '__main__':
    unittest.main()
