# ASR Tool – Automatic Speech Recognition

A command-line tool that converts spoken English in audio files into text using OpenAI's open-source **Whisper** model. After the model is downloaded once, it runs fully offline on your own machine (macOS and Windows supported).

## Team Members

| Name | Register Number |
|------|-----------------|
| Harini V | RA2311003050102 |
| Subhameedha BS | RA2311003050105 |
| Abishek Woolridge | RA2311003050155 |

## Features

- Transcribes `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.webm` and `.mp4` files
- English speech recognition (other languages can be selected with `--language`)
- Output as plain text, SRT subtitles (with timestamps) or JSON
- Optional Word Error Rate (WER) evaluation against a reference transcript
- Unit tests written with `pytest`

## Tools and Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Programming language |
| [OpenAI Whisper](https://github.com/openai/whisper) | Speech recognition model |
| PyTorch | Deep learning backend used by Whisper |
| FFmpeg | Audio decoding |
| pytest | Unit testing |
| Git and GitHub | Version control and hosting |

## Project Structure

```
asr-tool/
├── asr.py            # ASR tool (command-line interface and functions)
├── test_asr.py       # Unit tests
├── requirements.txt  # Python dependencies
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Install FFmpeg

- **macOS:** `brew install ffmpeg`
- **Windows:** `winget install ffmpeg` (or `choco install ffmpeg`), then restart the terminal

Check that it works with `ffmpeg -version`.

### 2. Clone the repository

```bash
git clone https://github.com/Hariniiii-iii/asr-tool.git
cd asr-tool
```

### 3. Create a virtual environment

- **macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows (Command Prompt or PowerShell):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## How to Run

Put an audio file (for example `sample.wav`) in the project folder, then run:

```bash
# Basic transcription (prints to the terminal)
python asr.py sample.wav

# Choose a model size and save subtitles
python asr.py sample.wav --model small --language en --format srt -o sample.srt

# Save as JSON
python asr.py sample.wav --format json -o sample.json

# Measure accuracy against a known transcript
python asr.py sample.wav --reference reference.txt
```

On macOS use `python3` if `python` is not found.

| Option | Description | Default |
|--------|-------------|---------|
| `--model` | `tiny`, `base`, `small`, `medium`, `large` (larger is more accurate but slower) | `base` |
| `--language` | Language code such as `en` | auto-detect |
| `--format` | `txt`, `srt` or `json` | `txt` |
| `-o, --output` | Save the result to a file | print to screen |
| `--reference` | Reference transcript file; prints the Word Error Rate | none |

The first run downloads the selected Whisper model, so it needs an internet connection and may take a moment.

## Testing

```bash
pytest -v
```

The tests cover timestamp formatting, SRT generation, Word Error Rate calculation, input validation and command-line error handling. They do not need the Whisper model or an internet connection.

## Example Run

```
$ python asr.py sample.wav --reference reference.txt
Hello, this is a test of the speech recognition tool.

Word Error Rate (WER): 0.00%
```

## How It Works

1. The audio path is validated (file exists and has a supported type).
2. Whisper loads the selected model and decodes the audio using FFmpeg.
3. The model returns the transcript along with timed segments.
4. The result is formatted as txt, srt or json.
5. If a reference transcript is given, the Word Error Rate is calculated using word-level edit distance.


This is the Site !!

<img width="1472" height="1514" alt="image" src="https://github.com/user-attachments/assets/d2bf6bb2-6e41-4f79-b34a-bd7cafb9f41e" />

