from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock
from src.app import App
import tkinter as tk

class TestApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
        self.app = App(self.root)

    def test_create_settings_widgets(self):
        # Test that settings widgets are created
        self.assertIsNotNone(self.app.mainframe)

    def test_create_run_widgets(self):
        # Test that run widgets are created
        self.assertIsNotNone(self.app.mainframe)

    def test_configure_grid(self):
        # Test that grid is configured
        self.app.configure_grid()
        self.assertEqual(self.app.mainframe.grid_info()['sticky'], 'nesw')
        self.assertEqual(self.app.mainframe.grid_info()['in'], self.app.root)

    def test_enable_widgets(self):
        # Test that widgets are enabled
        self.app.mainframe.grid()
        self.app.enable_widgets()
        self.assertEqual(self.app.mainframe.winfo_manager(), 'grid')

    def test_add_msg_text(self):
        # Test that message text is added
        self.app.add_msg_text('test message')
        self.assertIsNotNone(self.app.mainframe.winfo_children())

    def test_format_msg_text(self):
        # Test that message text is formatted
        result = 'test result'
        formatted_message = self.app.format_msg_text(result)
        current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        expected_message = f"\n[{current_time}] {result}"
        self.assertEqual(formatted_message, expected_message)

    @patch('tkinter.filedialog.askopenfilename', return_value='test file')
    def test_get_selected_file(self, mock_askopenfilename):
        # Call the get_selected_file method
        self.app.get_selected_file()
        # Check that the lselectedFile attribute is being set correctly
        self.assertEqual(self.app.lselectedFile.get(), 'test file')

    @patch('tkinter.filedialog.askdirectory', return_value='test dir')
    def test_get_selected_dir(self, mock_askdirectory):
        # Call the get_selected_dir method
        self.app.get_selected_dir()
        # Check that the lselectedDir attribute is being set correctly
        self.assertEqual(self.app.lselectedDir.get(), 'test dir')

    def test_get_filename(self):
        # Test that filename is returned
        filepath = 'test file'
        self.assertEqual(self.app.get_filename(filepath), 'test file')

    def test_update_progress_bar(self):
        # Test that progress bar is updated
        self.app.update_progress_bar(50, 100)
        self.assertIsNotNone(self.app.mainframe.winfo_children())

    def test_save_to_file(self):
        with patch.object(self.app, 'save_to_file') as mock_save_to_file:
            # Test that result is saved to file
            result = 'test result'
            self.app.save_to_file(result)
            mock_save_to_file.assert_called_once_with(result)

    def test_run_transcriber(self):
        with patch.object(self.app.wTranscriber, 'transcribe_with_progress') as mock_transcribe_with_progress:
            with patch.object(self.app, 'run_transcriber') as mock_run_transcriber:
                mock_run_transcriber.side_effect = lambda: mock_transcribe_with_progress()
                self.app.run_transcriber()
                mock_transcribe_with_progress.assert_called()

    def tearDown(self):
        self.root.destroy()  # Clean up the window

if __name__ == '__main__':
    unittest.main()