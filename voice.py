import sounddevice as sd
from scipy.io.wavfile import write

import librosa
import soundfile as sf
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3
import threading

def record_voice(filename, duration=10, fs=44100):
    """
    Record audio and save it as a WAV file.
    :param filename: Output file name.
    :param duration: Duration to record in seconds.
    :param fs: Sampling rate.
    """
    devices = sd.query_devices()
    default_input_device = None

    # Find a valid input device
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            default_input_device = i
            break

    if default_input_device is None:
        raise RuntimeError("No valid input device found for recording!")

    # Set the default input device
    sd.default.device = [default_input_device, None]
    print(f"Using input device: {sd.query_devices()[default_input_device]['name']}")

    # Record the audio
    print("Recording... Speak now!")
    voice_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()

    # Save the recorded audio
    write(filename, fs, (voice_data * 32767).astype('int16'))


# Function to blend voice with background music
def blend_voice_with_music(voice_file, music_file, output_file, pitch_shift_steps=-6, time_stretch_rate=0.9, voice_volume=0.9, music_volume=0.1):
    """
    Blend recorded voice with a pre-downloaded haunting background music.
    """
    voice_audio, voice_sr = librosa.load(voice_file, sr=None)
    voice_audio, _ = librosa.effects.trim(voice_audio, top_db=30)
    pitched_voice = librosa.effects.pitch_shift(voice_audio, sr=voice_sr, n_steps=pitch_shift_steps)
    slowed_voice = librosa.effects.time_stretch(pitched_voice, rate=time_stretch_rate)
    normalized_voice = slowed_voice / np.max(np.abs(slowed_voice))
    music_audio, music_sr = librosa.load(music_file, sr=voice_sr)

    if len(music_audio) < len(normalized_voice):
        music_audio = np.tile(music_audio, int(np.ceil(len(normalized_voice) / len(music_audio))))[:len(normalized_voice)]
    else:
        music_audio = music_audio[:len(normalized_voice)]

    blended_audio = (voice_volume * normalized_voice) + (music_volume * music_audio)
    blended_audio = blended_audio / np.max(np.abs(blended_audio))
    sf.write(output_file, blended_audio, voice_sr)


# Function to play music in the background
def play_background_music(music_file, stop_event):
    """
    Play background music in a loop until stop_event is set.
    :param music_file: Path to the background music file.
    :param stop_event: A threading event to stop the music playback.
    """
    music_audio, sr = librosa.load(music_file, sr=None)
    while not stop_event.is_set():
        sd.play(music_audio, samplerate=sr)
        sd.wait()


# Function to ask a question with a scary voice and simultaneous music and input
def ask_with_scary_voice(text, music_file, timeout=15):
    """
    Ask a question in a scary deep voice with background music and timeout for user input.
    :param text: The question to ask.
    :param music_file: Path to the background music file.
    :param timeout: Timeout in seconds for user input.
    :return: User's response to the question or None if timed out.
    """
    # Start background music in a separate thread
    stop_event = threading.Event()
    music_thread = threading.Thread(target=play_background_music, args=(music_file, stop_event))
    music_thread.start()

    # Ask the question using text-to-speech
    engine = pyttsx3.init()
    engine.setProperty('rate', 70)  # Slow down the speech rate
    engine.setProperty('volume', 1.0)  # Max volume
    voices = engine.getProperty('voices')

    # Select a deeper voice if available
    for voice in voices:
        if "male" in voice.name.lower():  # Look for a male voice for a deeper tone
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()  # Wait until TTS finishes speaking

    # Get the user's input with a timeout
    user_response = [None]

    def get_input():
        user_response[0] = input("Enter your answer: ")

    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout)

    # Stop the background music
    stop_event.set()
    music_thread.join()

    if input_thread.is_alive():
        print("Time's up! No answer received.")
        return None

    return user_response[0]


# Function to play audio
def play_audio(file_path):
    audio, sr = sf.read(file_path)
    sd.play(audio, samplerate=sr)
    sd.wait()


# Main program
if __name__ == "__main__":
    input_filename = "input.wav"
    music_filename = "haunting_music.wav"
    output_filename = "spooky_voice_with_music.wav"
    
    # Step 1: Ask for the user's name in their voice
    name = ask_with_scary_voice("Say out your name aloud : ", music_filename)
    print("Say out your name aloud : ")
    record_voice(input_filename, duration=10)
    play_audio(music_filename)
    
    # Step 2: Modulate the name into a scary voice and ask the first question
    #print("Processing your voice...")
    #blend_voice_with_music(input_filename, music_filename, output_filename)
    
    # Step 3: Ask the questions with simultaneous music and delay between questions
    fear = ask_with_scary_voice("What is your greatest fear?", music_filename)
    if fear is not None:
        print(f"Answer recorded: {fear}")
    else:
        print("No answer received for the first question.")
    
    # Wait 5 seconds before asking the next question

    hide_place = ask_with_scary_voice("What is your favorite place to hide?", music_filename)
    if hide_place is not None:
        print(f"Answer recorded: {hide_place}")
    else:
        print("No answer received for the second question.")

    print("Run Away!")