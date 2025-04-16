# Video to Text Transcription

This project extracts audio from a video file, transcribes it into English text using the Azure Speech API, and saves the transcription to a text file.

## Features
- Extracts audio from video files (supports multiple formats like MP4).
- Splits audio into manageable segments if necessary (default: 1-minute segments).
- Transcribes audio to text using Azure Speech-to-Text API.
- Saves the transcription to a text file for further editing.
- Cleans up temporary files after processing.
- Handles errors gracefully during audio processing and transcription.

## Prerequisites
- Python 3.8 or higher.
- Azure Speech API key and location.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/video_to_text.git
   cd video_to_text
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Azure Speech API key and location:
   - Open `main.py` and replace the placeholders for `AZURE_SPEECH_KEY` and `AZURE_AI_LOCATION` with your Azure credentials:
     ```python
     AZURE_SPEECH_KEY = "<your_azure_speech_api_key>"
     AZURE_AI_LOCATION = "<your_azure_ai_location>"
     ```

## Usage
1. Run the script with a video file as input:
   ```bash
   python main.py /path/to/video.mp4
   ```

2. The script will:
   - Extract audio from the video.
   - Transcribe the audio into text.
   - Save the transcription to a file named `<video_file_name>_transcription.txt`.
   - Open the transcription file for editing.

## Project Structure
```
video_to_text/
├── helper.py          # Contains utility functions for audio processing and transcription.
├── main.py            # Main script to run the transcription process.
├── requirements.txt   # Lists the required Python packages.
├── README.md          # Project documentation.
├── LICENSE            # License information.
└── .gitignore         # Files and directories to ignore in version control.
```

## Example
Suppose you have a video file named `example.mp4`. Run the following command:
```bash
python main.py example.mp4
```
The transcription will be saved to `example_transcription.txt` in the same directory.

## Notes
- Ensure the input file is in a supported format (e.g., MP4). Other formats may require adjustments.
- The Azure Speech API key and location must be set by the user in `main.py`. For better security, consider using environment variables or a configuration file.
- Temporary audio files created during processing will be automatically deleted after transcription.

## License
This project is licensed under the MIT License. See the LICENSE file for details.