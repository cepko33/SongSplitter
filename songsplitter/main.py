import argparse
import os
from frequency_splitter import split_frequency_bands
from source_separator import separate_sources

def main():
    parser = argparse.ArgumentParser(description="A script to split audio files by frequency bands or separate sources.")
    parser.add_argument("audio_file", help="Path to the input audio file.")
    parser.add_argument("--mode", choices=["frequency", "source"], required=True,
                        help="Choose 'frequency' to split by frequency bands or 'source' to separate sources.")
    parser.add_argument("--output_prefix", default="output",
                        help="Prefix for output files (used in 'frequency' mode).")
    parser.add_argument("--output_dir", default="separated_output",
                        help="Directory for output files (used in 'source' mode).")
    parser.add_argument("--bands", nargs='+', type=str,
                        help="Custom frequency bands as 'low_hz-high_hz' (e.g., '0-500 500-4000') (used in 'frequency' mode).")
    parser.add_argument("--format", default="wav", choices=["wav", "mp3"],
                        help="Output format for separated sources: 'wav' or 'mp3' (used in 'source' mode).")
    parser.add_argument("--mp3_bitrate", default=320, type=int,
                        help="Bitrate for MP3 output (used in 'source' mode, if format is 'mp3').")

    args = parser.parse_args()

    if not os.path.exists(args.audio_file):
        print(f"Error: Audio file '{args.audio_file}' not found.")
        return

    if args.mode == "frequency":
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
        split_frequency_bands(args.audio_file, args.output_prefix, custom_bands, args.format)
    elif args.mode == "source":
        separate_sources(args.audio_file, args.output_dir, args.format, args.mp3_bitrate)

if __name__ == "__main__":
    # Activate the virtual environment before running the script
    # This is a placeholder for local execution. In a deployed environment,
    # the virtual environment would typically be activated by the shell.
    # For demonstration purposes, we'll assume the environment is active
    # or the user will activate it manually.
    main()
