"""ASR tool: transcribe audio files to text using OpenAI Whisper.

Usage:
    python asr.py audio.wav
    python asr.py audio.mp3 --model small --language en --format srt -o out.srt
    python asr.py audio.wav --reference reference.txt   # also prints WER
"""

import argparse
import json
import re
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm", ".mp4"}


# ---------- helpers (no heavy dependencies, easy to unit test) ----------

def format_timestamp(seconds: float) -> str:
    """Convert seconds to an SRT timestamp: HH:MM:SS,mmm."""
    total_ms = int(round(seconds * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def segments_to_srt(segments) -> str:
    """Convert Whisper segments to SRT subtitle text."""
    blocks = []
    for i, seg in enumerate(segments, start=1):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        blocks.append(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n")
    return "\n".join(blocks)


def normalize_text(text: str) -> list:
    """Lowercase, strip punctuation and split into words."""
    text = re.sub(r"[^\w\s']", " ", text.lower())
    return text.split()


def word_error_rate(reference: str, hypothesis: str) -> float:
    """Word Error Rate = (substitutions + deletions + insertions) / reference words."""
    ref, hyp = normalize_text(reference), normalize_text(hypothesis)
    if not ref:
        raise ValueError("Reference text is empty.")
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, start=1):
        cur = [i]
        for j, h in enumerate(hyp, start=1):
            cost = 0 if r == h else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur
    return prev[-1] / len(ref)


def validate_audio_path(path: str) -> Path:
    """Check that the audio file exists and has a supported extension."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Audio file not found: {path}")
    if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{p.suffix}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )
    return p


# ---------- core ASR ----------

def transcribe(audio_path: str, model_name: str = "base", language: str = None) -> dict:
    """Transcribe an audio file and return Whisper's result dict."""
    p = validate_audio_path(audio_path)
    import whisper  # imported lazily so helpers/tests work without it

    model = whisper.load_model(model_name)
    return model.transcribe(str(p), language=language, fp16=False)


def render(result: dict, fmt: str) -> str:
    """Render a transcription result as txt, srt or json."""
    if fmt == "txt":
        return result["text"].strip()
    if fmt == "srt":
        return segments_to_srt(result["segments"])
    if fmt == "json":
        return json.dumps(
            {
                "language": result.get("language"),
                "text": result["text"].strip(),
                "segments": [
                    {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
                    for s in result["segments"]
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    raise ValueError(f"Unknown format: {fmt}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Speech-to-text using OpenAI Whisper.")
    parser.add_argument("audio", help="Path to the audio file")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base)")
    parser.add_argument("--language", default=None,
                        help="Language code, e.g. en, ta, hi (default: auto-detect)")
    parser.add_argument("--format", dest="fmt", default="txt",
                        choices=["txt", "srt", "json"], help="Output format")
    parser.add_argument("-o", "--output", default=None,
                        help="Write output to this file instead of printing")
    parser.add_argument("--reference", default=None,
                        help="Reference transcript file; prints Word Error Rate")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = transcribe(args.audio, args.model, args.language)
    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    except ImportError:
        print("Error: openai-whisper is not installed. Run: pip install -r requirements.txt",
              file=sys.stderr)
        return 1

    output = render(result, args.fmt)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Saved transcription to {args.output}")
    else:
        print(output)

    if args.reference:
        reference = Path(args.reference).read_text(encoding="utf-8")
        wer = word_error_rate(reference, result["text"])
        print(f"\nWord Error Rate (WER): {wer:.2%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
