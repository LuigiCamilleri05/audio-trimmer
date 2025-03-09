import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView  # Web-based waveform
from pydub import AudioSegment

class AudioTrimmerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Trimmer with Waveform")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Select File Button
        self.label = QLabel("No file selected")
        layout.addWidget(self.label)

        self.selectButton = QPushButton("Choose Audio File")
        self.selectButton.clicked.connect(self.select_file)
        layout.addWidget(self.selectButton)

        # WebView for waveform
        self.waveform = QWebEngineView()
        layout.addWidget(self.waveform)

        # Trim Button
        self.trimButton = QPushButton("Trim and Save")
        self.trimButton.clicked.connect(self.trim_audio)
        self.trimButton.setEnabled(False)  # Disabled until file is selected
        layout.addWidget(self.trimButton)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)")

        if file_path:
            self.audio_path = file_path
            self.label.setText(f"Selected: {os.path.basename(file_path)}")
            self.load_waveform(file_path)
            self.trimButton.setEnabled(True)  # Enable trimming

    def load_waveform(self, file_path):
        """ Loads waveform visualization using wavesurfer.js """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://unpkg.com/wavesurfer.js"></script>
        </head>
        <body>
            <div id="waveform"></div>
            <script>
                var wavesurfer = WaveSurfer.create({{
                    container: '#waveform',
                    waveColor: 'violet',
                    progressColor: 'purple'
                }});
                wavesurfer.load('file:///{file_path.replace("\\", "/")}');

                // Enable trimming
                wavesurfer.on('ready', function () {{
                    wavesurfer.addRegion({{
                        start: 1,
                        end: 3,
                        color: 'rgba(0, 255, 0, 0.2)'
                    }});
                }});
            </script>
        </body>
        </html>
        """
        self.waveform.setHtml(html)

    def trim_audio(self):
        """ Trims the audio based on user selection (placeholder values for now) """
        if self.audio_path:
            audio = AudioSegment.from_file(self.audio_path)

            start_time = 1000  # Placeholder (1s)
            end_time = 5000  # Placeholder (5s)

            trimmed_audio = audio[start_time:end_time]
            output_file, _ = QFileDialog.getSaveFileName(self, "Save Trimmed Audio", "", "MP3 Files (*.mp3);;WAV Files (*.wav)")

            if output_file:
                trimmed_audio.export(output_file, format="mp3" if output_file.endswith(".mp3") else "wav")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioTrimmerApp()
    window.show()
    sys.exit(app.exec())
