import argparse
import os
import torch as th
from demucs.apply import apply_model
from demucs.pretrained import get_model_from_args
from demucs.audio import AudioFile, save_audio
import argparse

def separate_sources(audio_path, output_dir="separated_output", output_format="wav", mp3_bitrate=320):
    """
    Separates an audio file into its constituent sources (e.g., drums, bass, melody, vocals).

    Args:
        audio_path (str): Path to the input audio file.
        output_dir (str): Directory to save the separated audio files.
    """
    print(f"Separating sources for '{audio_path}'...")

    # Create a dummy args object for get_model_from_args
    class DummyArgs:
        def __init__(self):
            self.model = "htdemucs"
            self.name = None
            self.repo = None
            self.segment = None
            self.stem = None
            self.verbose = False

    args = DummyArgs()
    model = get_model_from_args(args)
    model.cpu()
    model.eval()

    # Load the audio file
    wav = AudioFile(audio_path).read(
        streams=0,
        samplerate=model.samplerate,
        channels=model.audio_channels)
    
    ref = wav.mean(0)
    wav -= ref.mean()
    wav /= ref.std()

    # Apply the model
    device = "cuda" if th.cuda.is_available() else "cpu"
    sources = apply_model(model, wav[None], device=device, shifts=1,
                          split=True, overlap=0.25, progress=True,
                          num_workers=0, segment=None)[0]
    sources *= ref.std()
    sources += ref.mean()

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the separated sources
    for source, name in zip(sources, model.sources):
        ext = output_format
        filename_base = os.path.basename(audio_path).rsplit('.', 1)[0]
        output_path = os.path.join(output_dir, f"{filename_base}_{name}.{ext}")
        
        kwargs = {'samplerate': model.samplerate}
        if output_format == "mp3":
            kwargs['bitrate'] = mp3_bitrate

        save_audio(source, output_path, **kwargs)

    print(f"Separation complete. Separated sources saved to '{output_dir}'")

def main():
    parser = argparse.ArgumentParser(description="Separate an audio file into its constituent sources (e.g., drums, bass, melody).")
    parser.add_argument("audio_file", help="Path to the input audio file.")
    parser.add_argument("--output_dir", default="separated_output",
                        help="Directory to save the separated audio files.")

    parser.add_argument("--format", default="wav", choices=["wav", "mp3"],
                        help="Output format for separated sources: 'wav' or 'mp3'.")
    parser.add_argument("--mp3_bitrate", default=320, type=int,
                        help="Bitrate for MP3 output (if format is 'mp3').")

    args = parser.parse_args()

    separate_sources(args.audio_file, args.output_dir, args.format, args.mp3_bitrate)

if __name__ == "__main__":
    main()
