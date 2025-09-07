import numpy
import numpy as np
import librosa
import librosa.display
from modules import functions


# Extracts and returns the first
def extractAudioInfo(title, folder_name, expected_frequency):
    #Loading the voice sample to be analysed
    original_audio = f"InputAudio/{folder_name}/{title}"
    title = title[:-4]

    # Creates two variables, one is the audio in array from, and other sampling rate sr
    array_audio, sr = librosa.load(original_audio, mono=True, sr=44100)


    # Gets total sample number
    total_samples = len(array_audio)
    print("Audio converted to array successfully:", array_audio, "Audio length:", total_samples)


    # Saves time domain graph to appropriate folder, adjusts y-axis so that even low volume is visible
    functions.generate_time_domain_graph(array_audio=array_audio, title=title)


    # Performs FFT transformation on the audio array, then gets the
    # total number of positive frequency values that are contained
    # in a sample (from 1HZ to nyquist rate/2 Hz)
    fft_array_audio = np.fft.fft(array_audio)
    print("FFT array values:", fft_array_audio)
    magnitude_spectrum = np.abs(fft_array_audio)[:total_samples // 2]

    frequencies = np.fft.fftfreq(total_samples, 1 / sr)
    positive_frequencies = frequencies[:total_samples // 2]
    print("Positive frequencies:", positive_frequencies)

    # Creates an array with first x overtones from the audio
    overtones = functions.find_x_overtones(number_of_overtones=10, magnitude_spectrum=magnitude_spectrum,
                                           total_samples=total_samples,
                                           expected_fundamental_frequency=expected_frequency)

    # Normalises the array based on the fundamental amplitude
    fundamental_amplitude = overtones[0]
    overtones = numpy.delete(overtones, 0)
    overtones = overtones / fundamental_amplitude
    normalised_magnitude_spectrum = magnitude_spectrum / fundamental_amplitude

    # Saves the audio's frequency peaks array to the FrequencyPeaks folder
    np.savetxt(f'OutputArrays/FrequencyPeaks/{title}Peaks.txt', overtones)
    print("Frequency peaks saved to arrays in OutputArrays/FrequencyPeaks successfully\n")


    # Creates and saves normalised frequency domain graph to appropriate folder
    functions.generate_frequency_domain_graph(frequencies=positive_frequencies, magnitude_spectrum=normalised_magnitude_spectrum, title=title)


    # Creates and saves normalised frequency domain graph to appropriate folder
    functions.generate_frequency_domain_graph_log(frequencies=positive_frequencies, magnitude_spectrum=normalised_magnitude_spectrum, title=title, total_samples=total_samples, number_of_overtones=10)


