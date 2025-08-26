import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_frequency_bands(audio_path, output_prefix="output", bands=None, output_format="wav"):
    """
    Splits an audio file into different frequency bands.

    Args:
        audio_path (str): Path to the input audio file.
        output_prefix (str): Prefix for the output file names.
        bands (list of tuples): A list of (low_hz, high_hz) tuples defining the frequency bands.
                                If None, default bands (low, mid, high) will be used.
        output_format (str): The desired output format (e.g., "wav", "mp3", "flac").
    """
    audio = AudioSegment.from_file(audio_path)

    if bands is None:
        # Default bands: Low (0-500Hz), Mid (500-4000Hz), High (4000Hz-20000Hz)
        bands = [(0, 500), (500, 4000), (4000, 20000)]
        band_names = ["low", "mid", "high"]
    else:
        band_names = [f"{b[0]}-{b[1]}Hz" for b in bands]

    print(f"Splitting '{audio_path}' into {len(bands)} frequency bands...")

    for i, (low_hz, high_hz) in enumerate(bands):
        # Apply filters based on band definition
        if low_hz == 0 and high_hz == 0:
            # This case should ideally not happen with valid bands, but as a safeguard
            filtered_audio = audio
        elif low_hz == 0:
            # Only apply low-pass filter if low_hz is 0
            filtered_audio = audio.low_pass_filter(high_hz)
        elif high_hz == 0 or high_hz >= audio.frame_rate / 2: # high_hz at or above Nyquist
            # Only apply high-pass filter if high_hz is effectively infinite or at Nyquist
            filtered_audio = audio.high_pass_filter(low_hz)
        else:
            # Apply band-pass filter
            filtered_audio = audio.low_pass_filter(high_hz).high_pass_filter(low_hz)
        output_path = f"{output_prefix}_{band_names[i]}.{output_format}"
        filtered_audio.export(output_path, format=output_format)
        print(f"Exported {band_names[i]} band to '{output_path}'")
