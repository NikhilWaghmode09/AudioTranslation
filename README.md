# Audio Generation Script

## Description

This script generates audio files from text inputs using the ElevenLabs API. It allows users to specify test values and generates corresponding MP3 files. If an audio file already exists in the output directory, the script will skip generating that file.

## Requirements

To run this program, you'll need the following:

1. Python 3.x
2. `elevenlabs` Python package

## Setup

1. **Install Python 3.x**: Make sure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install the required Python package**:
    ```sh
    pip install elevenlabs
    ```

3. **Clone or download this repository**: Ensure that the directory structure is as follows:
    ```
    main/
    ├── output/
    │   ├── TranslatedVoice(Female).mp3
    │   ├── TranslatedVoice(Male).mp3
    │── Test1.wav
    │── Test2.wav
    ├── app.py
    ```

4. **Set your ElevenLabs API key**: Update the `API_KEY` variable in the `app.py` script with your ElevenLabs API key.

## Usage

1. **Navigate to the project directory**:
    ```sh
    cd path/to/your/project/directory
    ```

2. **Run the script**:
    ```sh
    python app.py "test_value1, test_value2, test_value3"
    ```

   You can also specify the output directory (optional):
    ```sh
    python app.py "test_value1, test_value2, test_value3" --output_dir "output_directory"
    ```

## Script Explanation

### `app.py`

- **Imports**:
    - `os`: For handling file and directory operations.
    - `argparse`: For parsing command-line arguments.
    - `elevenlabs`: For generating audio using the ElevenLabs API.

- **Functions**:
    - `generate_audio(client, test_value, output_filename)`: Generates audio for a given test value and saves it to the specified output filename.
    - `parse_arguments()`: Parses command-line arguments to get test values and the output directory.
    - `main()`: Main function to initialize the ElevenLabs client, process test values, and generate audio files.

- **Command-Line Arguments**:
    - `test_values`: Comma-separated list of test values to generate audio for.
    - `--output_dir`: Optional argument to specify the directory where audio files will be saved (default is "output_audio").

## Example

To generate audio files for "Hello" and "World", and save them to the default output directory:
```sh
python app.py "Hello, World"
