import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_frequency_bands(audio_path, output_prefix="output", bands=None):
    """
    Splits an audio file into different frequency bands.

    Args:
        audio_path (str): Path to the input audio file.
        output_prefix (str): Prefix for the output file names.
        bands (list of tuples): A list of (low_hz, high_hz) tuples defining the frequency bands.
                                If None, default bands (low, mid, high) will be used.
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
        output_path = f"{output_prefix}_{band_names[i]}.wav"
        filtered_audio.export(output_path, format="wav")
        print(f"Exported {band_names[i]} band to '{output_path}'")

def main():
    parser = argparse.ArgumentParser(description="Split an audio file into frequency bands.")
    parser.add_argument("audio_file", help="Path to the input audio file.")
    parser.add_argument("--output_prefix", default="output",
                        help="Prefix for the output frequency band files (e.g., 'song_low.wav').")
    parser.add_argument("--bands", nargs='+', type=str,
                        help="Custom frequency bands as 'low_hz-high_hz' (e.g., '0-500 500-4000').")

    args = parser.parse_args()

    custom_bands = None
    if args.bands:
        custom_bands = []
        for band_str in args.bands:
            try:
                low_hz, high_hz = map(int, band_str.split('-'))
                if low_hz >= high_hz:
                    raise ValueError("Low frequency must be less than high frequency.")
                custom_bands.append((low_hz, high_hz))
            except ValueError:
                print(f"Invalid band format: {band_str}. Please use 'low_hz-high_hz' (e.g., '0-500').")
                return

    split_frequency_bands(args.audio_file, args.output_prefix, custom_bands)

if __name__ == "__main__":
    main()
