"""
Project 12: The Local Audio Transcriber

Hidden Gem: `faster-whisper` — 4x faster than openai-whisper with the same
accuracy, using CTranslate2 for optimized inference.

What it does: Transcribes audio files to text using Whisper models.
Falls back to a simulated demo if faster-whisper isn't installed.
"""
import os
import time
import wave
import struct
import math


def generate_test_audio(filename="test_audio.wav", duration=3, freq=440):
    """Generate a test WAV file with a simple tone."""
    sample_rate = 16000
    num_samples = duration * sample_rate

    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        for i in range(num_samples):
            # Simple sine wave with fade
            t = i / sample_rate
            amplitude = 0.3 * math.sin(2 * math.pi * freq * t)
            fade = 1.0 - (t / duration) * 0.5
            value = int(amplitude * fade * 32767)
            wav.writeframes(struct.pack('<h', value))

    return filename


def transcribe_with_whisper(filepath):
    """Transcribe audio using faster-whisper."""
    from faster_whisper import WhisperModel

    print("Loading Whisper model (tiny)...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")

    print(f"Transcribing: {filepath}")
    start = time.time()
    segments, info = model.transcribe(filepath, beam_size=5)

    print(f"Language: {info.language} (prob: {info.language_probability:.2f})")
    print(f"Duration: {info.duration:.1f}s\n")

    full_text = []
    for segment in segments:
        print(f"[{segment.start:.1f}s → {segment.end:.1f}s] {segment.text.strip()}")
        full_text.append(segment.text.strip())

    elapsed = time.time() - start
    print(f"\nTranscribed in {elapsed:.2f}s")
    return " ".join(full_text)


def demo_mode(filepath):
    """Simulated transcription when faster-whisper isn't available."""
    print("--- Demo Mode (faster-whisper not installed) ---")
    print(f"\nAudio file: {filepath}")
    print(f"Duration: 3.0s")
    print(f"Language: en (prob: 0.99)")
    print(f"\n[0.0s → 3.0s] [simulated] This is a test audio recording.")
    print(f"\nTo enable real transcription:")
    print(f"  pip install faster-whisper")
    print(f"\nThe model downloads automatically on first run (~75MB for 'tiny').")


def main():
    print("--- Local Audio Transcriber ---")
    print("Using faster-whisper for offline speech-to-text\n")

    # Generate a test audio file
    audio_file = "test_audio.wav"
    if not os.path.exists(audio_file):
        print(f"Generating test audio: {audio_file}")
        generate_test_audio(audio_file, duration=3, freq=440)
        print(f"✓ Test audio created ({os.path.getsize(audio_file)} bytes)\n")

    try:
        transcribe_with_whisper(audio_file)
    except ImportError:
        demo_mode(audio_file)
    except Exception as e:
        print(f"Transcription error: {e}")
        demo_mode(audio_file)


if __name__ == "__main__":
    main()
