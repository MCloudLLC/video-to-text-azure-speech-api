import speech_recognition as sr
from pydub import AudioSegment
import os
import math

# Constants
SECOND_TO_MILLI = 60 * 1000  # Conversion factor: seconds to milliseconds
TMP_FILE_NAME = "_temp_audio"  # Temporary file prefix
SEGMENT_LENGTH = 1 * SECOND_TO_MILLI  # Segment length in milliseconds (1 minute)

def clean_up_temp_files(files_array):
    """
    Deletes temporary audio files created during processing.
    """
    print("Cleaning up temp files.")
    for file in files_array:
        if os.path.exists(file):
            print(f"Deleting file: {file}")
            os.remove(file)

def check_file_exists(input_file):
    """
    Checks if the input file exists and prints its name and directory.

    Args:
        input_file (str): Path to the input file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    if os.path.exists(input_file):
        file_name = os.path.basename(input_file)
        file_path = os.path.dirname(os.path.abspath(input_file))
        print(f"Filename: {file_name}")
        print(f"Directory: {file_path}")
        return True
    return False

def get_audio_channel(input_file):
    """
    Extracts and processes the audio channel from the input video file.

    Args:
        input_file (str): Path to the input video file.

    Returns:
        AudioSegment: Processed mono-channel audio with a sample rate of 16 kHz.
    """
    file_format = os.path.splitext(input_file)[1][1:]  # Extract file extension
    try:
        video = AudioSegment.from_file(input_file, format=file_format)
        audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        return audio
    except Exception as e:
        print(f"Error processing file {input_file}: {e}")
        return None

def load_audio_segments(audio_file):
    """
    Splits the audio file into smaller segments if it exceeds the segment length.

    Args:
        audio_file (AudioSegment): The audio file to be segmented.

    Returns:
        list: List of file paths to the exported audio segments.
    """
    audio_segments = []
    audio_length = len(audio_file)
    print("Exporting to WAV file(s).")

    if audio_length > SEGMENT_LENGTH:
        print("Audio larger than 1 minute, splitting into smaller segments.")
        num_segments = math.ceil(audio_length / SEGMENT_LENGTH)
        for i in range(num_segments):
            start_time = i * SEGMENT_LENGTH
            end_time = min((i + 1) * SEGMENT_LENGTH, audio_length)  # Ensure last segment doesn't exceed total length
            segment = audio_file[start_time:end_time]
            tmp_file = f"{TMP_FILE_NAME}_part{i + 1}.wav"
            segment.export(tmp_file, format="wav")
            audio_segments.append(tmp_file)
            print(f"Created file: {tmp_file}")
    else:
        tmp_file = f"{TMP_FILE_NAME}.wav"
        audio_file.export(tmp_file, format="wav")
        audio_segments.append(tmp_file)
        print(f"Created file: {tmp_file}")

    print("Export complete.")
    return audio_segments

def transcribe_audio_segments(audio_files, api_key, api_location):
    """
    Transcribes audio segments using Azure Speech-to-Text API.

    Args:
        audio_files (list): List of audio file paths to transcribe.
        api_key (str): Azure Speech API key.
        api_location (str): Azure Speech API location.

    Returns:
        list: List of transcribed text segments.
    """
    txt_array = []
    print("Transcribing WAV file(s).")
    recognizer = sr.Recognizer()

    for file in audio_files:
        try:
            with sr.AudioFile(file) as source:
                print(f"Transcribing file: {file}")
                recognizer.adjust_for_ambient_noise(source)
                audio_text = recognizer.record(source)
                # Recognize speech using Azure Speech-to-Text
                text, confidence = recognizer.recognize_azure(audio_text, key=api_key, location=api_location)
                txt_array.append(f"{text} ")  # Add space for concatenation
        except Exception as e:
            print(f"Error transcribing file {file}: {e}")

    print("Transcription complete.")
    return txt_array

def get_transcription_file(input_file):
    """
    Generates the output transcription file path.

    Args:
        input_file (str): Path to the input video file.

    Returns:
        str: Path to the transcription file.
    """
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    file_path = os.path.dirname(os.path.abspath(input_file))
    return os.path.join(file_path, f"{file_name}_transcription.txt")

def write_file(input_file, transcribed_text):
    """
    Writes the transcribed text to a file.

    Args:
        input_file (str): Path to the input video file.
        transcribed_text (list): List of transcribed text segments.
    """
    print("Creating transcription file.")
    txtfile_name = get_transcription_file(input_file)

    try:
        with open(txtfile_name, "w", encoding="utf-8") as file:
            for text in transcribed_text:
                file.write(text)
        print(f"Transcription saved to: {txtfile_name}")
    except Exception as e:
        print(f"Error writing transcription file: {e}")
