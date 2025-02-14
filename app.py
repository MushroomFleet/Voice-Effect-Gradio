import gradio as gr
import librosa
import soundfile as sf
import numpy as np
from scipy import signal

class VoiceEffects:
    def __init__(self, input_file):
        self.y, self.sr = librosa.load(input_file, sr=None)
        
    def add_reverb(self, room_size=0.8, damping=0.5):
        """
        Add reverb effect using convolution
        room_size: controls the size of the simulated room (0 to 1)
        damping: controls how quickly the reverb decays (0 to 1)
        """
        reverb_len = int(self.sr * room_size)
        impulse = np.exp(-damping * np.linspace(0, reverb_len, reverb_len))
        impulse = np.pad(impulse, (0, max(0, len(self.y) - len(impulse))), mode='constant')
        reverb_signal = signal.convolve(self.y, impulse, mode='same')
        self.y = 0.6 * self.y + 0.4 * reverb_signal
        
    def apply_frequency_filter(self, cutoff_freq, filter_type='lowpass', order=4):
        """
        Apply different types of frequency filters
        filter_type: 'lowpass', 'highpass', or 'bandpass'
        cutoff_freq: frequency cutoff in Hz
        """
        nyquist = self.sr / 2
        normalized_cutoff = cutoff_freq / nyquist
        
        if filter_type == 'lowpass':
            b, a = signal.butter(order, normalized_cutoff, btype='low')
        elif filter_type == 'highpass':
            b, a = signal.butter(order, normalized_cutoff, btype='high')
        elif filter_type == 'bandpass':
            b, a = signal.butter(order, [normalized_cutoff * 0.5, normalized_cutoff], btype='band')
            
        self.y = signal.filtfilt(b, a, self.y)
        
    def add_vibrato(self, freq=5.0, depth=0.3):
        """
        Add vibrato effect
        freq: vibrato frequency in Hz
        depth: vibrato depth (0 to 1)
        """
        t = np.arange(len(self.y)) / self.sr
        mod = depth * np.sin(2 * np.pi * freq * t)
        delay_samples = (mod * self.sr).astype(int)
        vibrato_signal = np.zeros_like(self.y)
        for i in range(len(self.y)):
            index = i - delay_samples[i]
            if 0 <= index < len(self.y):
                vibrato_signal[i] = self.y[index]
        self.y = vibrato_signal
        
    def change_formants(self, shift_factor=1.2):
        """
        Modify voice character by shifting formants
        shift_factor: factor to shift formants (>1 higher, <1 lower)
        """
        D = librosa.stft(self.y)
        D_mag, D_phase = librosa.magphase(D)
        D_mag_stretched = np.zeros_like(D_mag)
        for i in range(D_mag.shape[1]):
            D_mag_stretched[:, i] = np.interp(
                np.linspace(0, 1, D_mag.shape[0]),
                np.linspace(0, 1, D_mag.shape[0]),
                D_mag[:, i]
            )
        D_modified = D_mag_stretched * D_phase
        self.y = librosa.istft(D_modified)
        
    def add_echo(self, delay_time=0.3, decay=0.5):
        """
        Add echo effect
        delay_time: echo delay in seconds
        decay: echo decay factor (0 to 1)
        """
        delay_samples = int(self.sr * delay_time)
        echo_signal = np.zeros_like(self.y)
        if delay_samples < len(self.y):
            echo_signal[delay_samples:] = self.y[:-delay_samples] * decay
        self.y = self.y + echo_signal
        
    def add_distortion(self, gain=2.0, threshold=0.5):
        """
        Add distortion effect
        gain: input gain
        threshold: clipping threshold
        """
        distorted = self.y * gain
        distorted = np.clip(distorted, -threshold, threshold)
        if np.max(np.abs(distorted)) != 0:
            distorted = distorted / np.max(np.abs(distorted))
        self.y = distorted
        
    def save(self, output_file):
        """Save the processed audio"""
        sf.write(output_file, self.y, self.sr)

def process_audio(input_audio,
                  room_size, damping,
                  cutoff_freq, filter_type,
                  vibrato_freq, vibrato_depth,
                  shift_factor,
                  delay_time, decay,
                  gain, threshold):
    # input_audio is a filepath from Gradio Audio component
    effects = VoiceEffects(input_audio)
    effects.add_reverb(room_size=room_size, damping=damping)
    effects.apply_frequency_filter(cutoff_freq, filter_type=filter_type)
    effects.add_vibrato(freq=vibrato_freq, depth=vibrato_depth)
    effects.change_formants(shift_factor=shift_factor)
    effects.add_echo(delay_time=delay_time, decay=decay)
    effects.add_distortion(gain=gain, threshold=threshold)
    output_file = "modified_voice.wav"
    effects.save(output_file)
    return output_file

# Define Gradio interface
audio_input = gr.Audio(type="filepath", label="Upload or Record Audio")
room_size_slider = gr.Slider(0.0, 1.0, value=0.8, step=0.1, label="Reverb Room Size")
damping_slider = gr.Slider(0.0, 1.0, value=0.3, step=0.1, label="Reverb Damping")
cutoff_slider = gr.Slider(300, 5000, value=1000, step=100, label="Filter Cutoff Frequency (Hz)")
filter_radio = gr.Radio(choices=["lowpass", "highpass", "bandpass"], value="lowpass", label="Filter Type")
vibrato_freq_slider = gr.Slider(1.0, 10.0, value=6.0, step=0.5, label="Vibrato Frequency (Hz)")
vibrato_depth_slider = gr.Slider(0.0, 1.0, value=0.2, step=0.1, label="Vibrato Depth")
shift_factor_slider = gr.Slider(0.5, 2.0, value=1.1, step=0.1, label="Formant Shift Factor")
delay_slider = gr.Slider(0.1, 1.0, value=0.2, step=0.1, label="Echo Delay Time (s)")
decay_slider = gr.Slider(0.1, 1.0, value=0.3, step=0.1, label="Echo Decay")
gain_slider = gr.Slider(1.0, 5.0, value=1.5, step=0.1, label="Distortion Gain")
threshold_slider = gr.Slider(0.1, 1.0, value=0.7, step=0.1, label="Distortion Threshold")

iface = gr.Interface(
    fn=process_audio,
    inputs=[
        audio_input,
        room_size_slider, damping_slider,
        cutoff_slider, filter_radio,
        vibrato_freq_slider, vibrato_depth_slider,
        shift_factor_slider,
        delay_slider, decay_slider,
        gain_slider, threshold_slider
    ],
    outputs=gr.Audio(type="filepath", label="Modified Audio"),
    title="Voice Effects Processor",
    description="Upload or record an audio file to apply various voice effects and preview the modified audio. The processed file will be saved as 'modified_voice.wav'."
)

if __name__ == "__main__":
    iface.launch()
