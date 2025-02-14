# Voice Effects Processor

A Python application to apply multiple creative voice effects on audio recordings. This application uses Gradio to present an interactive web interface for processing audio files using various DSP techniques, including reverb, frequency filtering, vibrato, formant shifting, echo, and distortion.

## Features

- **Reverb**: Simulates room acoustics by convolving the audio signal with a generated impulse response.
- **Frequency Filtering**: Provides options for lowpass, highpass, or bandpass filtering to shape the audio spectrum.
- **Vibrato**: Modulates the pitch periodically to add a vibrato effect.
- **Formant Shifting**: Alters the voice characteristics by shifting formants.
- **Echo**: Adds a delayed and decaying repetition of the audio.
- **Distortion**: Clips the audio signal with gain and threshold controls for a distorted effect.

## Installation

1. **Clone or Download the Repository**  
   Obtain the project files on your local machine.

2. **Set Up a Python Environment**  
   It is recommended to use Python 3.7 or later. You can create a virtual environment by running:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**  
   Install all necessary packages using the following command:
   ```
   pip install -r requirements.txt
   ```
   The dependencies include `gradio`, `librosa`, `soundfile`, `numpy`, and `scipy`.

4. **Optional Batch Scripts**  
   Use the provided batch files for convenience:
   - `install.bat` to install dependencies.
   - `start-gui.bat` to launch the Gradio interface.

## Usage

1. **Run the Application**  
   Launch the application by executing:
   ```
   python app.py
   ```
   Alternatively, you can run:
   ```
   start-gui.bat
   ```
   to open the Gradio user interface.

2. **Interact with the Gradio Interface**  
   Upon launch, a browser window will open with the following options:
   - **Audio Input**: Upload or record an audio file.
   - **Adjust Effects**: Modify parameters using sliders and radio buttons for:
     - Reverb (Room Size, Damping)
     - Frequency Filtering (Cutoff Frequency, Filter Type)
     - Vibrato (Frequency, Depth)
     - Formant Shifting (Shift Factor)
     - Echo (Delay Time, Decay)
     - Distortion (Gain, Threshold)
   - **Process Audio**: Click the button to apply the effects.
   - **Output**: The processed audio is saved as `modified_voice.wav` and can be previewed or downloaded directly from the interface.

## About app.py

The core functionality is implemented in `app.py`:

- **VoiceEffects Class**  
  Implements methods to apply various voice effects:
  - `add_reverb`: Adds a reverb effect using convolution.
  - `apply_frequency_filter`: Applies a lowpass, highpass, or bandpass filter.
  - `add_vibrato`: Adds a vibrato effect to modulate the voice.
  - `change_formants`: Shifts formants to modify the voice character.
  - `add_echo`: Introduces an echo effect with delay and decay.
  - `add_distortion`: Applies distortion by clipping the audio signal.

- **process_audio Function**  
  This function:
  - Instantiates the `VoiceEffects` class with the input audio file.
  - Sequentially applies all the voice effects based on the user's parameters.
  - Saves the final processed output as `modified_voice.wav`.

- **Gradio Interface**  
  The interface components in `app.py` allow users to:
  - Upload or record an audio file.
  - Adjust parameters for different effects.
  - Preview the processed audio in real-time.

This README provides detailed instructions for installation, usage, and an overview of what `app.py` does. Enjoy exploring the creative possibilities of voice effects processing!
