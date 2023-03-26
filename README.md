# Audio Augmentation Script

This Python script takes a folder of audio files as input and augments them using the audiomentations library. The script applies TimeStretch, PitchShift, and Shift effects. The output files are resampled to 44100 Hz and saved as WAV files. It also provides options to split stereo files into mono files, split longer files into 30-second chunks, and add 5 seconds of silence at the end of each file.

## Installation

1. Make sure you have Python 3.6 or higher installed.

2. Install the required libraries:

```pip install numpy soundfile audiomentations```

## Basic Usage
Run the script using the command line with the required arguments:

´´´python audio_augmentation.py input_folder output_folder --split_stereo --add_silence´´´

input_folder: Path to the input folder containing audio files
output_folder: Path to the output folder for the augmented files
--split_stereo: (Optional) Flag to split stereo files into two mono files
--add_silence: (Optional) Flag to add 5 seconds of silence at the end of each sound file

## Example:

´´´python audio_augmentation.py ./input_audio ./output_audio --split_stereo --add_silence´´´

This command will process audio files in the input_audio folder, apply the augmentations, split stereo files into mono files, add 5 seconds of silence at the end, and save the resulting files in the output_audio folder.

## Notes
The input folder can contain audio files in various formats such as WAV, FLAC, OGG, AIFF, and MP3.
The script will output WAV files with a sample rate of 44100 Hz.
The output filenames will contain information about the channel and chunk number. If augmentations are applied, "_augmented" will be added to the filename.
