import os
import argparse
import numpy as np
import soundfile as sf
import resampy

def is_supported_audio_file(filename):
    supported_extensions = ['.wav', '.flac', '.ogg', '.aiff', '.mp3']
    _, ext = os.path.splitext(filename)
    return ext.lower() in supported_extensions

def change_speed(audio, speed_change):
    return np.interp(np.arange(0, len(audio), speed_change), np.arange(0, len(audio)), audio)

def resample_audio(input_audio, original_sample_rate=44100, target_sample_rate=44100):
    if original_sample_rate != target_sample_rate:
        audio_resampled = resampy.resample(input_audio, original_sample_rate, target_sample_rate)
    else:
        audio_resampled = input_audio
    return audio_resampled    

def process_audio_file(input_file, output_folder, chunk_duration, split_stereo, add_silence, speed_change):
    audio, sample_rate = sf.read(input_file)
    if split_stereo and audio.ndim == 2:
        channels = [audio[:, 0], audio[:, 1]]
    else:
        channels = [audio]
    for i, channel in enumerate(channels):
        if chunk_duration > 0:
            chunk_duration_s = chunk_duration * sample_rate
            for start_idx in range(0, len(channel), chunk_duration_s):
                end_idx = start_idx + chunk_duration_s
                chunk = channel[start_idx:end_idx]

                if add_silence:
                    silence = np.zeros(int(5 * sample_rate))
                    chunk = np.concatenate((chunk, silence))

                #output original
                audio_resampled = resample_audio(chunk, original_sample_rate=sample_rate, target_sample_rate=44100)
                output_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_ch{i}_chunk{start_idx // chunk_duration_s}_orig.wav")
                sf.write(output_filename, chunk, 44100)
                print(output_filename)

                if speed_change != 0.0:
                    #make random speed change within speedchange minus and plus
                    speed_change_rnd = np.random.uniform(1.0 - speed_change, 1.0 + speed_change)

                    chunk = change_speed(chunk, speed_change_rnd)
                    chopchunk = chunk[0:chunk_duration_s]
                    output_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_ch{i}_chunk{start_idx // chunk_duration_s}_aug.wav")
                    sf.write(output_filename, chopchunk, 44100)
                    print(output_filename)
        else:
            audio_resampled = resample_audio(channel, original_sample_rate=sample_rate, target_sample_rate=44100)
            output_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_ch{i}_orig.wav")
            sf.write(output_filename, audio_resampled, 44100)
            print(output_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Speed Change")
    parser.add_argument("input_folder", help="Path to the input folder containing audio files")
    parser.add_argument("output_folder", help="Path to the output folder for processed files")
    parser.add_argument("--chunk_duration", type=int, default=30, help="Duration of each chunk in seconds (default: 30 seconds")
    parser.add_argument("--split_stereo", action="store_true", help="Split stereo files into two mono files")
    parser.add_argument("--add_silence", action="store_true", help="Add 5 seconds of silence at the end of each sound file")
    parser.add_argument("--speed_change", type=float, default=0.0, help="Speed change factor 0.0-0.9 (default: 0.0, no change)")
    args = parser.parse_args()

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    for root, _, files in os.walk(args.input_folder):
        for file in files:
            if is_supported_audio_file(file):
                input_file = os.path.join(root, file)
                process_audio_file(input_file, args.output_folder, args.chunk_duration, args.split_stereo, args.add_silence, args.speed_change)
