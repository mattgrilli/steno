# steno

# Audio Transcription and ChatGPT Integration Tool

This project is a desktop application designed to streamline the process of transcribing audio files and leveraging OpenAI's ChatGPT for further processing and analysis. It's built with Python, utilizing the Tkinter library for the GUI, Whisper for transcription, and the OpenAI API for ChatGPT integration.

## Features

- **Audio Transcription**: Transcribe audio files to text using OpenAI's Whisper model.
- **ChatGPT Integration**: Send transcriptions to ChatGPT for summarization, question answering, or further analysis.
- **File Management**: Easily manage audio and transcription files within the application.
- **Responsive UI**: A user-friendly interface that adapts to different screen sizes and resolutions.
- **Export Options**: Export transcriptions and ChatGPT responses to txt.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mattgrilli/steno.git

    Install Dependencies:
        Ensure Python 3.8+ is installed on your system.
        Install required Python packages:

        bash

        pip install -r requirements.txt

Usage

    Start the Application:
        Run the main_app.py script to launch the application:

        bash

        python main_app.py

    Transcribing Audio:
        Use the "Select Audio File" button to choose an audio file for transcription.
        The transcription will appear in the central display field.
    Interacting with ChatGPT:
        Select a prompt or create a new one using the "Manage Prompts" button.
        Send the transcription to ChatGPT using the "Send to ChatGPT" button.
        The ChatGPT response will be appended to the transcription in the display field.
    Exporting Data:
        Use the "Export" button to save the transcription and ChatGPT responses to a file.

Contributing

Contributions to the project are welcome! Here's how you can contribute:

    Fork the Repository: Click the "Fork" button on the GitHub repository page.
    Create a Feature Branch:

    bash

git checkout -b feature/YourFeature

Commit Your Changes:

bash

git commit -am 'Add some feature'

Push to the Branch:

bash

    git push origin feature/YourFeature

    Open a Pull Request: Go to the repository page on GitHub and click the "Pull request" button.

License

This project is licensed under the MIT License - see the LICENSE file for details.
