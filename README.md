# SongSplitter

SongSplitter is a Python script that allows you to process audio files in two main ways:
1. **Frequency Band Splitting**: Extract specific frequency ranges (e.g., low, mid, high) from an audio file.
2. **Source Separation**: Separate an audio file into its constituent instrumental/vocal sources (e.g., drums, bass, melody, vocals) using the Demucs model.

## Setup

1.  **Create a virtual environment and install dependencies:**
    ```bash
    mkdir songsplitter
    python3 -m venv songsplitter/.venv
    source songsplitter/.venv/bin/activate
    pip install pydub numpy scipy librosa demucs
    ```

2.  **Place the scripts:**
    Ensure `frequency_splitter.py`, `source_separator.py`, and `main.py` are in the `songsplitter/` directory.

## Usage

First, activate your virtual environment:
```bash
source songsplitter/.venv/bin/activate
```

Then, you can use `main.py` with different modes:

### Mode 1: Frequency Band Splitting

This mode allows you to split an audio file into different frequency bands.

**Default Bands (Low, Mid, High):**
```bash
python songsplitter/main.py your_audio_file.mp3 --mode frequency --output_prefix your_song
```
This will create `your_song_low.wav`, `your_song_mid.wav`, and `your_song_high.wav`.

**Custom Bands:**
You can define your own frequency bands using the `--bands` argument. Provide a space-separated list of `low_hz-high_hz` ranges.
```bash
python songsplitter/main.py your_audio_file.mp3 --mode frequency --output_prefix your_song_custom --bands "0-200" "200-1000" "1000-5000"
```
This will create `your_song_custom_0-200Hz.wav`, `your_song_custom_200-1000Hz.wav`, and `your_song_custom_1000-5000Hz.wav`.

### Mode 2: Source Separation

This mode uses the Demucs model to separate an audio file into its individual sources (e.g., drums, bass, other, vocals).

```bash
python songsplitter/main.py your_audio_file.mp3 --mode source --output_dir separated_tracks
```
This will create a directory named `separated_tracks` (or your specified `--output_dir`) containing the separated audio files (e.g., `your_audio_file/drums.wav`, `your_audio_file/bass.wav`, `your_audio_file/other.wav`, `your_audio_file/vocals.wav`).

**Note on Demucs:** The first time you run the source separation, Demucs might download the pre-trained model, which can take some time and requires an internet connection.

## Example
To run the frequency splitting on an example file:
```bash
# Assuming you have an audio file named 'example.mp3' in the current directory
python songsplitter/main.py example.mp3 --mode frequency --output_prefix example_bands
```

To run the source separation on an example file:
```bash
# Assuming you have an audio file named 'example.mp3' in the current directory
python songsplitter/main.py example.mp3 --mode source --output_dir example_separated
