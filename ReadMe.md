# WSCOACH

there is the code developed for the paper **"Using Real-time Auditory Feedback for the Reduction of Unwanted Words in Daily Communication"**.

## Table of Contents

- [WSCOACH](#wscoach)
  - [Table of Contents](#table-of-contents)
    - [Features](#features)
    - [Installation](#installation)
    - [Usage](#usage)
  - [FasterWhisperModel Module](#fasterwhispermodel-module)
    - [Features](#features-1)
    - [Installation](#installation-1)
    - [Usage](#usage-1)
  - [Record Module](#record-module)
    - [Features](#features-2)
    - [Installation](#installation-2)
    - [Usage](#usage-2)
  - [TTS Module](#tts-module)
    - [Features](#features-3)
    - [Installation](#installation-3)
    - [Usage](#usage-3)
  - [Contributing](#contributing)
  - [License](#license)

### Features

- **Word Detection**: Recognizes specific words or phrases in a given text string.
- **Tracking**: Keeps track of the number of times each word is detected.

### Installation

No additional installation is required for this module. However, make sure that the required dependencies are installed in your Python environment, the required dependencies is listed in the `requirement.txt`.

### Usage

If you want a easy show of the WSCOACH, just run the `HTML_render.py` and then you can use the basic features of WSCOACH.

## FasterWhisperModel Module

The `FasterWhisperModel` module provides a wrapper for the Faster-Whisper ASR (Automatic Speech Recognition) model. It allows for efficient transcription of audio files or arrays, with a focus on faster processing.

### Features

- **Fast Transcription**: Utilizes the Faster-Whisper ASR model for efficient and quick audio transcription.
- **File and Array Transcription**: Supports transcription from both audio files and arrays.

### Installation

No additional installation is required for this module. However, make sure that the required dependencies are installed in your Python environment.

### Usage

1. Import the `FasterWhisperModel` class into your Python script.

   ```python
   from faster_whisper import FasterWhisperModel
   ```
2. Create an instance of the `FasterWhisperModel` class.

   ```python
   model = FasterWhisperModel()
   ```
3. Use the `TranscribeFile` method to transcribe audio from a file.

   ```python
   text = model.TranscribeFile("./path/to/audio/file.wav")
   print(f"Transcribed Text: {text}")
   ```
4. Use the `TranscribeArray` method to transcribe audio from a NumPy array.

   ```python
   text = model.TranscribeArray(audio_array)
   print(f"Transcribed Text: {text}")
   ```

## Record Module

The `Record` module provides functionality for recording audio using the PyAudio library. It captures audio input from a specified input device and writes it to a WAV file. Additionally, it supports playing back recorded audio.

### Features

- **Audio Recording**: Records audio input from a specified input device.
- **Buffer Management**: Manages an internal buffer to store audio data efficiently.
- **Wave File Creation**: Writes recorded audio to a WAV file.
- **Audio Playback**: Supports playback of recorded audio.

### Installation

No additional installation is required for this module. However, make sure that the required dependencies are installed in your Python environment.

### Usage

1. Import the `Record` class into your Python script.

   ```python
   from Record import Record
   ```
2. Create an instance of the `Record` class.

   ```python
   record = Record()
   ```
3. Optionally, set the input and output devices using the provided methods.

   ```python
   input_device_names = record.get_device_input_names()
   output_device_names = record.get_device_output_names()

   record.set_device_input_index("Your_Input_Device_Name")
   record.set_device_output_index("Your_Output_Device_Name")
   ```
4. Start the recording thread.

   ```python
   record.start()
   ```
5. Optionally, capture the audio buffer.

   ```python
   audio_buffer = record.GetBuffer()
   ```
6. Optionally, end the recording.

   ```python
   record.endRecord()
   ```
7. Optionally, play the recorded audio.

   ```python
   record.playWave("Your_Wave_File_Name", detect=detect_instance, first_name="Your_First_Name")
   ```

## TTS Module

The `TTS` module utilizes the pyttsx4 library to convert text into speech and save the generated audio as WAV files. It provides the ability to adjust the speech rate and save individual words or phrases as separate audio files.

### Features

- **Text-to-Speech Conversion**: Converts input text into speech.
- **Adjustable Speech Rate**: Allows the user to set the speech rate.
- **Saving to WAV Files**: Saves the generated speech as WAV files.

### Installation

No additional installation is required for this module. However, make sure that the required dependencies are installed in your Python environment.

### Usage

1. Import the `TTS` class into your Python script.

   ```python
   from TTS import TTS
   ```
2. Create an instance of the `TTS` class.

   ```python
   tts = TTS()
   ```
3. Optionally, set the speech rate.

   ```python
   tts.SetRate(2.0)
   ```
4. Use the `Word2File` method to convert and save text as a WAV file.

   ```python
   tts.Word2File("Hello World")
   ```

## Contributing

If you would like to contribute to the development of this project or report issues, please contract us.

## License

This project is open source and available under the [MIT License]().
