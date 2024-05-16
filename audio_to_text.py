import os
import speech_recognition as sr
from pydub import AudioSegment
import sys
import string
from langdetect import detect

def transcribe_audio(audio_file_path):
    # Convert mp3 to wav
    sound = AudioSegment.from_mp3(audio_file_path)
    wav_file_path = audio_file_path[:-4] + ".wav"
    sound.export(wav_file_path, format="wav")

    # Create a speech recognition object
    recognizer = sr.Recognizer()

    # Open the audio file
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)  # Get the audio data

    try:
        # Detect the language of the audio
        language = detect_language(audio_file_path)

        # Transcribe the audio data
        if language == 'ja':
            transcription = recognizer.recognize_google(audio_data, language='ja-JP')
        else:
            transcription = recognizer.recognize_google(audio_data, language='en-US')

        # Capitalize the first letter of the transcription
        transcription = capitalize_transcription(transcription)

        # Add a question mark if the transcription is a question
        if is_question(transcription):
            transcription += '?'
        else:
            transcription += '.'

        return transcription # Return Unicode string
    except sr.UnknownValueError:
        return "Unable to understand the speech"
    except sr.RequestError as e:
        return f"Google Speech Recognition error: {e}"
    finally:
        # Clean up: remove temporary wav file
        os.remove(wav_file_path)

def capitalize_transcription(transcription):
    # Split the transcription into words
    words = transcription.split()

    # Capitalize proper nouns
    for i, word in enumerate(words):
        if i == 0 or not word[0].islower():
            words[i] = word.capitalize()

    # Join the words back into a string
    return ' '.join(words)

def save_transcription(transcription, audio_file_path):
    # Get the file name and extension
    file_name, _ = os.path.splitext(audio_file_path)

    # Get the language code
    language = detect_language(audio_file_path)

    # Determine the language code suffix
    if language == 'ja':
        lang_suffix = '_jp'
    elif language == 'en':
        lang_suffix = '_en'
    else:
        lang_suffix = '_' + language

    # Create the text file name with language code suffix
    txt_file_path = file_name + lang_suffix + ".txt"

    # Write the transcription result to the text file
    with open(txt_file_path, "w", encoding='utf-8') as txt_file:
        txt_file.write(transcription)

def detect_language(audio_file_path):
    # Use langdetect library to detect language
    try:
        language = detect(open(audio_file_path, 'rb').read())
    except:
        language = 'en'  # Default to English if language detection fails
    return language

def is_question(text):
    # Check if the text starts with a form of "be" verb
    if text.strip().lower().startswith(('am', 'is', 'are', 'was', 'were', 'be', 'being', 'been')):
        return True

    # Check if the text starts with a question word
    question_words = ['who', 'what', 'when', 'where', 'why', 'how', 'did', 'do', 'does', 'can', 'could', 'will', 'would', 'shall', 'should', 'may', 'might', 'must']
    if any(word in text.lower().split() for word in question_words):
        return True

    # Check if the text starts with "do" or "does"
    if text.strip().lower().startswith(('do', 'does')):
        return True

    return False

def transcribe_directory(directory_path):
    # Iterate over all files in the directory
    for file_name in os.listdir(directory_path):
        # Check if the file is an MP3 audio file
        if file_name.lower().endswith('.mp3'):
            audio_file_path = os.path.join(directory_path, file_name)
            transcription = transcribe_audio(audio_file_path)
            if transcription:
                save_transcription(transcription, audio_file_path)
                print(f"Transcription saved for {audio_file_path}.")
            else:
                print(f"Failed to transcribe {audio_file_path}.")

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python3 audio_to_text.py <path_to_audio_file_or_directory>")
        return

    # Get the path passed as argument
    path = sys.argv[1]

    # Check if the path is a directory or a file
    if os.path.isdir(path):
        transcribe_directory(path)
    elif os.path.isfile(path) and path.lower().endswith('.mp3'):
        transcription = transcribe_audio(path)
        if transcription:
            save_transcription(transcription, path)
            print(f"Transcription saved as {path}.txt")
        else:
            print(f"Failed to transcribe {path}.")
    else:
        print("Error: Please specify an existing MP3 audio file or directory containing MP3 audio files.")

if __name__ == "__main__":
    main()

