# LoFiConvert

LoFiConvert is a Python command-line tool that transforms any song into a lofi remix. It achieves this by separating vocals, slowing down the instrumental, applying a low-pass filter for a muffled sound, and adding ambient effects.

## Features

- **Vocal Separation:** Utilizes Spleeter to isolate instrumental tracks.
- **Tape-Slow Effect:** Adjusts playback speed and pitch to create a classic slowed-down sound.
- **Low-Pass Filter:** Applies a muffled, "underwater" audio effect.
- **Ambient Noise:** Adds subtle white noise for texture (can be customized with real vinyl crackle).
- **Automatic BPM Detection:** Intelligently calculates the slowdown factor based on the song's original BPM and a target lofi BPM.

## Prerequisites

Before running LoFiConvert, ensure you have the following installed:

1.  **Python 3.10**: The project is configured to run with Python version 3.10.
2.  **FFmpeg**: A cross-platform solution to record, convert and stream audio and video. Spleeter and Pydub rely on this.

## Installation

This project uses `uv` for dependency management, which is a fast Python package installer and resolver.

1.  **Install `uv` (if you don't have it):**
    ```bash
    pip install uv
    ```
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/usoy410/loficonvert.git
    cd loficonvert
    ```
3.  **Install project dependencies:**
    ```bash
    uv sync
    ```

## Usage

Run the `loficonvert.py` script with your audio file. The output will be an instrumental track in an `output/` directory and the final lofi remix MP3 in the current directory.

```bash
uv run loficonvert.py <path_to_your_song.mp3>
```

### Examples:

- **Basic conversion (automatic BPM detection, target 80 BPM):**

  ```bash
  uv run loficonvert.py "my_favorite_track.mp3"
  ```

- **Specify a manual slowdown factor:**

  ```bash
  uv run loficonvert.py "my_favorite_track.mp3" --slow_factor 0.9
  ```

- **Specify a target BPM (e.g., for a 75 BPM lofi track):**
  ```bash
  uv run loficonvert.py "my_favorite_track.mp3" --target_bpm 75
  ```

## Output

- **Instrumental:** The separated instrumental track will be saved in a new directory named `output/` within your project folder.
- **Lofi Remix:** The final lofi remixed MP3 will be saved in the same directory where you ran the command, with `_lofi_remix.mp3` appended to the original filename (e.g., `my_favorite_track_lofi_remix.mp3`).
