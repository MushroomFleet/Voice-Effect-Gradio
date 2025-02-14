import librosa
import soundfile as sf
import numpy as np
from scipy import signal
from scipy.signal import lfilter

class VoiceEffects:
    def __init__(self, input_file):
        self.y, self.sr = librosa.load(input_file)
        
    def add_reverb(self, room_size=0.8, damping=0.5):
        """
        Add reverb effect using convolution
        room_size: controls the size of the simulated room (0 to 1)
        damping: controls how quickly the reverb decays (0 to 1)
        """
        # Create a simple impulse response
        reverb_len = int(self.sr * room_size)
        impulse = np.exp(-damping * np.linspace(0, reverb_len, reverb_len))
        impulse = np.pad(impulse, (0, len(self.y) - len(impulse)))
        
        # Apply convolution
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
        # Create time array
        t = np.arange(len(self.y)) / self.sr
        
        # Create modulation signal
        mod = depth * np.sin(2 * np.pi * freq * t)
        
        # Create time-varying delay
        delay_samples = (mod * self.sr).astype(int)
        
        # Apply vibrato using variable delay
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
        # Get the spectral envelope
        D = librosa.stft(self.y)
        D_mag, D_phase = librosa.magphase(D)
        
        # Stretch the magnitude spectrogram
        D_mag_stretched = np.zeros_like(D_mag)
        for i in range(D_mag.shape[1]):
            D_mag_stretched[:, i] = np.interp(
                np.linspace(0, 1, D_mag.shape[0]),
                np.linspace(0, 1, D_mag.shape[0]),
                D_mag[:, i]
            )
            
        # Reconstruct with modified formants
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
        echo_signal[delay_samples:] = self.y[:-delay_samples] * decay
        self.y = self.y + echo_signal
        
    def add_distortion(self, gain=2.0, threshold=0.5):
        """
        Add distortion effect
        gain: input gain
        threshold: clipping threshold
        """
        # Apply gain
        distorted = self.y * gain
        
        # Apply soft clipping
        distorted = np.clip(distorted, -threshold, threshold)
        
        # Normalize
        distorted = distorted / np.max(np.abs(distorted))
        
        self.y = distorted
        
    def save(self, output_file):
        """Save the processed audio"""
        sf.write(output_file, self.y, self.sr)

# Example usage
if __name__ == "__main__":
    # Create an instance with input file
    effects = VoiceEffects("input.wav")
    
    # Apply various effects
    effects.add_reverb(room_size=0.8, damping=0.3)
    effects.apply_frequency_filter(1000, filter_type='lowpass')
    effects.add_vibrato(freq=6.0, depth=0.2)
    effects.change_formants(shift_factor=1.1)
    effects.add_echo(delay_time=0.2, decay=0.3)
    effects.add_distortion(gain=1.5, threshold=0.7)
    
    # Save the result
    effects.save("modified_voice.wav")