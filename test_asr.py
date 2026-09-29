import pytest

import asr


def test_format_timestamp():
    assert asr.format_timestamp(0) == "00:00:00,000"
    assert asr.format_timestamp(3661.5) == "01:01:01,500"


def test_segments_to_srt():
    segments = [
        {"start": 0.0, "end": 2.5, "text": " Hello world"},
        {"start": 2.5, "end": 4.0, "text": " Second line"},
    ]
    srt = asr.segments_to_srt(segments)
    assert "1\n00:00:00,000 --> 00:00:02,500\nHello world" in srt
    assert "2\n00:00:02,500 --> 00:00:04,000\nSecond line" in srt


def test_wer_identical_is_zero():
    assert asr.word_error_rate("the cat sat", "The cat sat!") == 0.0


def test_wer_one_substitution():
    assert asr.word_error_rate("the cat sat", "the dog sat") == pytest.approx(1 / 3)


def test_wer_empty_reference_raises():
    with pytest.raises(ValueError):
        asr.word_error_rate("", "anything")


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        asr.validate_audio_path("does_not_exist.wav")


def test_unsupported_extension(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_text("hi")
    with pytest.raises(ValueError):
        asr.validate_audio_path(str(f))


def test_render_formats():
    result = {
        "language": "en",
        "text": " Hello world",
        "segments": [{"start": 0.0, "end": 1.0, "text": " Hello world"}],
    }
    assert asr.render(result, "txt") == "Hello world"
    assert "-->" in asr.render(result, "srt")
    assert '"text": "Hello world"' in asr.render(result, "json")


def test_cli_missing_file_returns_error(capsys):
    assert asr.main(["missing.wav"]) == 1
    assert "not found" in capsys.readouterr().err
