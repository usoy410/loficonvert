import os
import argparse
import librosa
from spleeter.separator import Separator
from pydub import AudioSegment
from pydub.generators import WhiteNoise
import numpy as np


def remove_vocals(input_file, output_dir="output"):
    """
    Isolates the instrumental from a song file using Spleeter.
    """
    # Initialize Spleeter with the '2stems' model (Vocals + Accompaniment)
    separator = Separator("spleeter:2stems")

    # This will create a folder with 'vocals.wav' and 'accompaniment.wav'
    separator.separate_to_file(input_file, output_dir)

    # Return the path to the instrumental track
    song_name = os.path.splitext(os.path.basename(input_file))[0]
    instrumental_path = os.path.join(output_dir, song_name, "accompaniment.wav")

    print(f"Vocals removed. Instrumental saved at: {instrumental_path}")
    return instrumental_path


def make_lofi(input_path, output_path, slow_factor=0.85):
    """
    Applies lofi effects to an audio file.
    """
    # Load the instrumental
    beat = AudioSegment.from_file(input_path)

    # THE TAPE SLOW EFFECT
    # change the sample rate to "trick" the computer into playing it slower and deeper
    new_sample_rate = int(beat.frame_rate * slow_factor)
    lofi_beat = beat._spawn(beat.raw_data, overrides={"frame_rate": new_sample_rate})

    # Convert it back to standard 44.1kHz so it plays on all devices,
    # but keep the slow/deep pitch
    lofi_beat = lofi_beat.set_frame_rate(44100)

    # LOW PASS FILTER (The "Underwater" muffled sound)
    # cut off frequencies above 3000Hz
    lofi_beat = lofi_beat.low_pass_filter(3000)

    # ADD VINYL CRACKLE (Optional Texture)
    # Here, we generate white noise as a substitute.
    noise = WhiteNoise().to_audio_segment(duration=len(lofi_beat), volume=-50)
    lofi_beat = lofi_beat.overlay(noise)

    # Export
    lofi_beat.export(output_path, format="mp3")
    print(f"Lofi beat created: {output_path}")


def detect_bpm(audio_path):
    """
    Detects the BPM of an audio file.
    """
    y, sr = librosa.load(audio_path)
    bpm, _ = librosa.beat.beat_track(y=y, sr=sr)

    # extract the single number (scalar) to do math with it.
    if isinstance(bpm, np.ndarray) or hasattr(bpm, "item"):
        bpm = bpm.item()
    # -----------------------

    print(f"Detected BPM: {bpm}")
    return bpm


def convert_to_lofi(my_song_path, slow_factor=None, target_bpm=80):
    """
    Full pipeline to convert a song to a lofi remix.
    """
    # Remove Vocals
    # Check if we are already inputting an instrumental (saves time if re-running)
    if "accompaniment" in my_song_path:
        print("Input appears to be an instrumental already. Skipping vocal separation.")
        instrumental_file = my_song_path
    else:
        print("Separating vocals... (This might take a moment)")
        instrumental_file = remove_vocals(my_song_path)

    # Calculate slowdown factor if not provided
    if slow_factor is None:
        print("Detecting BPM to calculate slowdown...")
        original_bpm = detect_bpm(instrumental_file)

        # Ensure we have a valid number before calculating
        if original_bpm and original_bpm > 0:
            slow_factor = target_bpm / original_bpm
            print(
                f"Calculated slow factor for target BPM of {target_bpm}: {slow_factor:.2f}"
            )
        else:
            print("Could not detect BPM, using default slow factor.")
            slow_factor = 0.85
    else:
        print(f"Using provided slow factor: {slow_factor}")

    # Apply Lofi Effects
    print("Applying Lofi effects...")
    base_name = os.path.splitext(os.path.basename(my_song_path))[0]
    final_output = f"{base_name}_lofi_remix.mp3"

    make_lofi(instrumental_file, final_output, slow_factor=slow_factor)

    print(f"Done! Check your folder for {final_output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a song to a Lofi beat.")
    parser.add_argument("input_song", help="The path to the song file to convert.")
    parser.add_argument(
        "--slow_factor",
        type=float,
        default=None,
        help="Manually set the slowdown factor (e.g., 0.85). Overrides automatic BPM detection.",
    )
    parser.add_argument(
        "--target_bpm", type=int, default=80, help="Target BPM for the lofi remix."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_song):
        print(f"Error: Input file not found at {args.input_song}")
    else:
        convert_to_lofi(args.input_song, args.slow_factor, args.target_bpm)
