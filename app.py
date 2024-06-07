import os
import argparse
import speech_recognition as sr
from pydub import AudioSegment
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from elevenlabs.client import ElevenLabs

# Define your ElevenLabs API key here
API_KEY = "dc8332c257a341e48c10649c799995c8"

# Function to recognize speech from an audio file
def recognize_speech_from_file(file_path, lang='auto'):
    print(f"Recognizing speech from file: {file_path}")

    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
        try:
            recognized_text = r.recognize_google(audio, language=lang)
            print(f"Recognized text: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

# Function to translate text from one language to another
def translate_text(text, source_lang, target_lang):
    print(f"Translating text from {source_lang} to {target_lang}")
    translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    print(f"Translated text: {translated_text}")
    return translated_text

# Function to save translated text to an audio file using ElevenLabs
def save_speech_to_file(text, output_path):
    print(f"Saving translated speech to file: {output_path}")
    client = ElevenLabs(api_key=API_KEY)

    # Generate audio using ElevenLabs
    audio_generator = client.generate(
        text=text,
        voice="50YSQEDPA2vlOxhCseP4",  # for FEMALE voice
        # voice="LrnwgcdTLxc99sutUxGU",  # for MALE voice
        model="eleven_multilingual_v2"
    )

    # Save the audio directly to the target format (MP3)
    with open(output_path, "wb") as file:
        for audio_chunk in audio_generator:
            file.write(audio_chunk)

    print(f"Saved translated speech to {output_path}")

def main(input_file, output_dir=None, input_lang='en', output_lang='en', output_filename='TranslatedVoice.mp3'):
    # Set the output directory to the same as input directory if not specified
    if output_dir is None:
        output_dir = os.path.dirname(input_file)

    # Recognize speech from the input file
    speech_text = recognize_speech_from_file(input_file, lang=input_lang)
    if not speech_text:
        print("No speech text recognized.")
        return

    # Transliterate if necessary
    if input_lang not in ('auto', 'en'):
        transliterated_text = transliterate(speech_text, sanscript.ITRANS, sanscript.DEVANAGARI)
    else:
        transliterated_text = speech_text

    # Translate the recognized speech text
    translated_text = translate_text(transliterated_text, source_lang=input_lang, target_lang=output_lang)

    # Prepare the output file path
    output_file = os.path.join(output_dir, output_filename)

    # Save the translated text to an audio file
    save_speech_to_file(translated_text, output_path=output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate speech from an audio file and save the translated speech to an audio file.")
    parser.add_argument("input_file", type=str, help="Path to the input audio file (WAV format)")
    parser.add_argument("--output_dir", type=str, help="Directory to save the output audio file (default: same as input file directory)")
    parser.add_argument("--input_lang", type=str, default="en", help="Language of the input audio (default: English)")
    parser.add_argument("--output_lang", type=str, default="en", help="Language for the translated audio (default: English)")
    parser.add_argument("--output_filename", type=str, default="TranslatedVoice.mp3", help="Name of the output audio file (default: TranslatedVoice.mp3)")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Input file {args.input_file} does not exist.")
        exit(1)

    if args.output_dir and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    main(args.input_file, args.output_dir, input_lang=args.input_lang, output_lang=args.output_lang, output_filename=args.output_filename)
