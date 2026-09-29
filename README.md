# ASR Tool – Automatic Speech Recognition

A command-line tool that converts speech in audio files into text using OpenAI's open-source **Whisper** model. It runs fully offline on your machine after the model is downloaded once.

## Features

- Transcribes `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.webm`, `.mp4`
- Automatic language detection (or choose one with `--language`)
- Output as plain text, SRT subtitles (with timestamps), or JSON
- Optional Word Error Rate (WER) evaluation against a reference transcript
- Unit tests with `pytest`

## Tools and Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Programming language |
| [OpenAI Whisper](https://github.com/openai/whisper) | Speech recognition model |
| PyTorch | Backend used by Whisper |
| FFmpeg | Audio decoding |
| pytest | Testing |
| Git / GitHub | Version control and hosting |

## Project Structure

```
asr-tool/
├── asr.py            # ASR tool (CLI + functions)
├── test_asr.py       # Unit tests
├── requirements.txt  # Python dependencies
├── .gitignore
└── README.md
```

## Setup

1. **Install FFmpeg**
   - Windows: `winget install ffmpeg` (or `choco install ffmpeg`)
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt install ffmpeg`

2. **Clone the repository and create a virtual environment**
   ```bash
   git clone https://github.com/<your-username>/asr-tool.git
   cd asr-tool
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
# Basic transcription (prints to terminal)
python asr.py sample.wav

# Choose model size and language, save as subtitles
python asr.py sample.mp3 --model small --language en --format srt -o sample.srt

# Save as JSON
python asr.py sample.wav --format json -o sample.json

# Evaluate accuracy against a known transcript
python asr.py sample.wav --reference reference.txt
```

| Option | Description | Default |
|--------|-------------|---------|
| `--model` | `tiny`, `base`, `small`, `medium`, `large` (bigger = more accurate, slower) | `base` |
| `--language` | Language code such as `en`, `hi`, `ta` | auto-detect |
| `--format` | `txt`, `srt`, `json` | `txt` |
| `-o, --output` | Save output to a file | print to screen |
| `--reference` | Reference transcript file, prints WER | none |

## Testing

```bash
pytest -v
```

The tests cover timestamp formatting, SRT generation, WER calculation, input validation and CLI error handling. They do not need the Whisper model or an internet connection.

## Sample Result

Add your own test run here, for example:

```
$ python asr.py sample.wav --reference reference.txt
Hello, this is a test of the speech recognition tool.

Word Error Rate (WER): 0.00%
```

## How It Works

1. The audio path is validated (exists, supported type).
2. Whisper loads the selected model and decodes the audio with FFmpeg.
3. The model returns text plus timed segments.
4. The result is rendered as txt, srt or json.
5. If a reference transcript is provided, WER is computed using word-level edit distance.

## Author

Your Name – your course / roll number
