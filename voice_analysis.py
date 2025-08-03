import sounddevice as sd
import numpy as np
import scipy.fft
import wavio

def record_audio(duration=5, fs=44100, filename="voice.wav"):
    print("🎙️ Recording... Speak for 5 seconds.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, audio, fs, sampwidth=2)
    print(f"✅ Saved: {filename}")
    return audio.flatten(), fs

def analyze_frequency(audio, fs):
    # Apply FFT
    N = len(audio)
    fft_data = scipy.fft.fft(audio)
    fft_freqs = scipy.fft.fftfreq(N, d=1/fs)
    
    # Only take positive frequencies
    positive_freqs = fft_freqs[:N//2]
    positive_fft = np.abs(fft_data[:N//2])

    # Find peak frequency
    peak_index = np.argmax(positive_fft)
    peak_freq = positive_freqs[peak_index]
    return peak_freq

def get_voice_tone(peak_freq):
    if peak_freq < 170:
        return "Calm"
    elif 170 <= peak_freq <= 300:
        return "Anxious"
    else:
        return "Energetic"

# Main Execution
if __name__ == "__main__":
    audio, fs = record_audio()
    peak_freq = analyze_frequency(audio, fs)
    tone = get_voice_tone(peak_freq)
    
    print(f"📊 Peak Frequency: {peak_freq:.2f} Hz")
    print(f"🧠 Voice Tone Analysis: {tone}")
