import os
import tkinter as tk
from tkinter import ttk, filedialog
from src.transcriptionSaver import TranscriptionSaver
import src.whisperTranscriber as wt
import threading
from datetime import datetime

class App:
    def __init__(self, root):
        self.wTranscriber = wt.WhisperTranscriber()

        self.root = root
        self.root.title('TTrans')

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.create_settings_widgets()
        self.create_run_widgets()
        self.configure_grid()

    def create_settings_widgets(self):
        self.settingsLf = ttk.Labelframe(self.mainframe, text='Settings')
        self.settingsLf.grid(column=0, row=0, columnspan=5, sticky=(tk.N, tk.E, tk.W))

        languages = self.wTranscriber.get_languages()
        languages.sort()
        self.lName = tk.StringVar(value='english')
        self.languagesCb = ttk.Combobox(self.settingsLf, textvariable=self.lName)
        self.languagesCb['values'] = languages
        self.languagesCb.state(['readonly'])
        self.languagesLbl = ttk.Label(self.settingsLf, text='Audio Language')

        self.languagesLbl.grid(column=0, row=0, sticky=(tk.E), padx=5)
        self.languagesCb.grid(column=1, row=0, columnspan=4, sticky=(tk.N, tk.E, tk.W), padx=5)

        models = self.wTranscriber.get_models()
        self.lModel = tk.StringVar(value=models[0])
        self.modelsCb = ttk.Combobox(self.settingsLf, textvariable=self.lModel, values=models, state='readonly')
        self.modelsLbl = ttk.Label(self.settingsLf, text='Model')
        
        self.modelsLbl.grid(row=1, column=0, sticky=(tk.E), padx=5)
        self.modelsCb.grid(row=1, column=1, columnspan=4, sticky=(tk.E,tk.W), padx=5)

        self.fileLbl = ttk.Label(self.settingsLf, text='Audio file')
        self.lselectedFile = tk.StringVar()
        self.selectedFileLbl = ttk.Label(self.settingsLf, textvariable=self.lselectedFile, anchor='w')
        self.fileBtn = ttk.Button(self.settingsLf, text='Browse...', default='active', command=self.get_selected_file)
        
        self.fileLbl.grid(column=0, row=2, sticky=(tk.E), padx=5)
        self.selectedFileLbl.grid(column=1, row=2, columnspan=3, sticky=(tk.E,tk.W), padx=5)
        self.fileBtn.grid(column=4, row=2, sticky=(tk.E), padx=5)

        self.dirlbl = ttk.Label(self.settingsLf, text='Output folder')
        self.lselectedDir = tk.StringVar()
        self.selectedDirLbl = ttk.Label(self.settingsLf, textvariable=self.lselectedDir, anchor='w')
        self.dirBtn = ttk.Button(self.settingsLf, text='Browse...', default='active', command=self.get_selected_dir)
        
        self.dirlbl.grid(column=0, row=3, sticky=(tk.E), padx=5)
        self.selectedDirLbl.grid(column=1, row=3, columnspan=4, sticky=(tk.E,tk.W), padx=5)
        self.dirBtn.grid(column=4, row=3, sticky=(tk.E), padx=5)

    def create_run_widgets(self):
        self.runLf = ttk.Labelframe(self.mainframe,text='Progress')
        self.runLf.grid(row=1,column=0,columnspan=5,sticky=(tk.E,tk.W,tk.S))
        self.runLf.columnconfigure(0,weight=1)
        self.runLf.rowconfigure(0,weight=1)

        self.testLbl = ttk.Label(self.runLf,text='')
        self.testLbl.grid(row=0,column=0,sticky=(tk.W),padx=5)

        self.runBtn = ttk.Button(self.runLf,text='Run',command=self.run_transcriber)
        self.runBtn.grid(row=0,column=4,sticky=(tk.E),padx=5)

        self.lprogress = tk.DoubleVar()
        self.progressBar = ttk.Progressbar(self.runLf,variable=self.lprogress, maximum=100)
        self.progressBar.grid(row=1,column=0,columnspan=5,sticky=(tk.E,tk.W),padx=5)

        self.msgTxt = tk.Text(self.runLf,wrap='word',height=15,state='disabled')
        self.msgTxt.grid(row=2,column=0,columnspan=5,sticky=(tk.E,tk.W,tk.S),padx=5)

    def configure_grid(self):
        for i in range(5):
            self.mainframe.columnconfigure(i, weight=1)
            self.settingsLf.columnconfigure(i, weight=1)
            self.runLf.columnconfigure(i, weight=1)

    def enable_widgets(self, enable: bool = True):
        new_state = '!disabled' if enable else tk.DISABLED

        self.languagesCb.state([new_state])
        self.modelsCb.state([new_state])
        self.fileBtn.state([new_state])
        self.dirBtn.state([new_state])
        self.runBtn.state([new_state])

    def add_msg_text(self,text):
        self.msgTxt.configure(state='normal')
        self.msgTxt.insert('end',self.format_msg_text(text))
        self.msgTxt.see('end')
        self.msgTxt.configure(state='disabled')

    def format_msg_text(self, text):
        current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        formatted_message = f"\n[{current_time}] {text}"
        return formatted_message

    def get_selected_file(self):
        selectedfile = filedialog.askopenfilename()
        self.lselectedFile.set(selectedfile)

        dir = os.path.dirname(selectedfile)
        self.lselectedDir.set(dir)

    def get_selected_dir(self):
        selectedDir = filedialog.askdirectory()
        self.lselectedDir.set(selectedDir)

    def get_filename(self, filepath):
        return os.path.splitext(os.path.basename(filepath))[0]

    def update_progress_bar(self, current, total):
        self.lprogress.set((current / total) * 100)
        self.root.update_idletasks()

    def save_to_file(self, result):
        self.add_msg_text('Creating output files...')
        # self.add_msg_text(result)
        tSaver = TranscriptionSaver(result
                                    ,'all'
                                    ,self.lselectedDir.get()
                                    ,self.get_filename(self.lselectedFile.get()))
        tSaver.save()
        self.enable_widgets()
        self.add_msg_text('Done!')

    def run_transcriber(self):
        if(not self.lselectedFile):
            self.add_msg_text('No file selected.')
            return
        elif(not self.lselectedDir):
            self.add_msg_text('No dir selected.')
            return
        
        try:
            self.update_progress_bar(0,1)
            self.enable_widgets(False)

            self.add_msg_text('Setting language...')
            self.wTranscriber.set_language(self.lName.get())

            self.add_msg_text('Setting model...')
            self.wTranscriber.set_model(self.lModel.get())

            file_name = os.path.basename(self.lselectedFile.get())
            self.add_msg_text(f'Reading {file_name}...')
            # result = self.wTranscriber.transcribe(self.lselectedFile.get())
            transcription_thread = threading.Thread(target=lambda: self.wTranscriber.transcribe_with_progress(
                    self.lselectedFile.get(), self.update_progress_bar, self.save_to_file))
            transcription_thread.start()

        except Exception as e:
            self.add_msg_text(f'error: {e}')
            self.enable_widgets()


