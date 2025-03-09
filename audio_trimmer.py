import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QLineEdit, QMessageBox
from pydub import AudioSegment

class AudioTrimmerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Trimmer')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Select File
        self.label = QLabel('Select an audio file:')
        layout.addWidget(self.label)

        self.selectButton = QPushButton('Choose File')
        self.selectButton.clicked.connect(self.select_file)
        layout.addWidget(self.selectButton)

        # Start time input
        self.start_label = QLabel('Start Time (seconds):')
        layout.addWidget(self.start_label)
        self.start_input = QLineEdit(self)
        layout.addWidget(self.start_input)

        # End time input
        self.end_label = QLabel('End Time (seconds):')
        layout.addWidget(self.end_label)
        self.end_input = QLineEdit(self)
        layout.addWidget(self.end_input)

        # Trim button
        self.trimButton = QPushButton('Trim Audio')
        self.trimButton.clicked.connect(self.trim_audio)
        layout.addWidget(self.trimButton)

        self.setLayout(layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)")
        
        if file_path:
            self.audio_path = file_path
            self.label.setText(f'Selected: {file_path.split("/")[-1]}')

    def trim_audio(self):
        try:
            start_time = int(self.start_input.text()) * 1000  # Convert to milliseconds
            end_time = int(self.end_input.text()) * 1000

            audio = AudioSegment.from_file(self.audio_path)
            trimmed_audio = audio[start_time:end_time]

            output_file, _ = QFileDialog.getSaveFileName(self, "Save Trimmed Audio", "", "MP3 Files (*.mp3);;WAV Files (*.wav)")

            if output_file:
                trimmed_audio.export(output_file, format="mp3" if output_file.endswith(".mp3") else "wav")
                QMessageBox.information(self, "Success", "Audio trimmed and saved successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioTrimmerApp()
    window.show()
    sys.exit(app.exec())
