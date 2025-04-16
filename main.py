import os
import sys
import helper

# Constants for Azure Speech API
AZURE_SPEECH_KEY = "<your_azure_speech_api_key>"  # Replace with your Azure Speech API key
AZURE_AI_LOCATION = "<your_azure_ai_location>"    # Replace with your Azure AI location

def main():
    """
    Main function to handle the video-to-text transcription process.
    """
    # Ensure the input file is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_video_file>")
        sys.exit(1)

    # Get the input file path from the command-line argument
    input_file = sys.argv[1]

    # Check if the input file exists
    if not helper.check_file_exists(input_file):
        print("Error: File does not exist or the path is invalid.")
        sys.exit(1)

    try:
        # Step 1: Extract and process the audio channel from the video
        audio = helper.get_audio_channel(input_file)
        if audio is None:
            print("Error: Failed to process the audio channel.")
            sys.exit(1)

        # Step 2: Split the audio into smaller segments if necessary
        audio_files = helper.load_audio_segments(audio)

        # Step 3: Transcribe the audio segments using Azure Speech-to-Text API
        transcribed_text = helper.transcribe_audio_segments(
            audio_files, api_key=AZURE_SPEECH_KEY, api_location=AZURE_AI_LOCATION
        )

        # Step 4: Write the transcribed text to a file
        helper.write_file(input_file, transcribed_text)

        # Step 5: Clean up temporary audio files
        helper.clean_up_temp_files(audio_files)

        # Step 6: Open the transcription file for editing
        transcription_file = helper.get_transcription_file(input_file)
        os.system(f"start {transcription_file}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()