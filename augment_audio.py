import os
import argparse
import numpy as np
import soundfile as sf
from audiomentations import Compose, TimeStretch, PitchShift, Shift

def is_supported_audio_file(filename):
    supported_extensions = ['.wav', '.flac', '.ogg', '.aiff', '.mp3']
    _, ext = os.path.splitext(filename)
    return ext.lower() in supported_extensions

def process_audio_file(input_file, output_folder, split_stereo, add_silence, augmentations):
    audio, sample_rate = sf.read(input_file)
    if split_stereo and audio.ndim == 2:
        channels = [audio[:, 0], audio[:, 1]]
    else:
        channels = [audio]
    for i, channel in enumerate(channels):
        chunk_duration = 30 * sample_rate
        for start_idx in range(0, len(channel), chunk_duration):
            end_idx = start_idx + chunk_duration
            chunk = channel[start_idx:end_idx]
            if add_silence:
                silence = np.zeros(int(5 * sample_rate))
                chunk = np.concatenate((chunk, silence))
            output_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_ch{i}_chunk{start_idx // chunk_duration}.wav")
            sf.write(output_filename, chunk, 44100)
            if augmentations is not None:
                augmented_chunk = augmentations(samples=chunk, sample_rate=44100)
                output_filename_augmented = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_ch{i}_chunk{start_idx // chunk_duration}_augmented.wav")
                sf.write(output_filename_augmented, augmented_chunk, 44100)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Augmentation")
    parser.add_argument("input_folder", help="Path to the input folder containing audio files")
    parser.add_argument("output_folder", help="Path to the output folder for augmented files")
    parser.add_argument("--split_stereo", action="store_true", help="Split stereo files into two mono files")
    parser.add_argument("--add_silence", action="store_true", help="Add 5 seconds of silence at the end of each sound file")
    args = parser.parse_args()
    augmentations = Compose([
        TimeStretch(min_rate=0.95, max_rate=1.05, p=1.0),
        PitchShift(min_semitones=-2, max_semitones=2, p=1.0),
        Shift(min_fraction=-0.2, max_fraction=0.2, p=1.0),
    ])
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    for root, _, files in os.walk(args.input_folder):
        for file in files:
            if is_supported_audio_file(file):
                input_file = os.path.join(root, file)
                process_audio_file(input_file, args.output_folder, args.split_stereo, args.add_silence, augmentations)
