import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os

from fontTools.ttLib.woff2 import bboxFormat


# Creates a time domain representation graph of the audio array, adjusting the y limits based on the max/min values of the normalised wav audio signal strength, ensuring that even quiet audio is discernible
# Saves graph to the designated folder, with title as the filename
def generate_time_domain_graph(array_audio, title, sr=44100, figsize=(15, 17)):
    graph_limits = max(max(array_audio), abs(min(array_audio)))

    plt.figure(figsize=figsize)
    plt.subplot(3, 1, 1)
    librosa.display.waveshow(array_audio, sr=sr)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Normalised signal strength")
    plt.ylim((-graph_limits, graph_limits))
    plt.savefig(f"Graphs/TimeDomain/{title}.png", bbox_inches='tight')
    print(f"Time domain graph for {title} saved successfully to Graphs/TimeDomain/")
    return


# Creates a frequency domain representation graph of the audio array, with 22050 (Half of 44100Hz sample rate) represented by default on teh x-axis
# Saves graph to the f"Graphs/FrequencyDomain/{title}.png"
def generate_frequency_domain_graph(frequencies, magnitude_spectrum, title, xlim=22050):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, magnitude_spectrum)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title(f'Frequency Spectrum of {title}')
    plt.grid(True)
    plt.xlim(0, xlim)
    plt.savefig(f"Graphs/FrequencyDomain/{title}.png")
    print(f"Frequency domain graph for {title} saved successfully to Graphs/FrequencyDomain/")
    return


# Creates a frequency domain representation graph of the audio array in log form
# Saves graph to the f"Graphs/FrequencyDomainLog/{title}.png"
def generate_frequency_domain_graph_log(frequencies, magnitude_spectrum, title, total_samples, number_of_overtones, sample_rate=44100):

    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, magnitude_spectrum)
    plt.xscale("log")
    plt.xlabel('Frequency (Hz) (log scale)')
    plt.ylabel('Amplitude')
    plt.title(f'Frequency Spectrum of {title}')
    plt.grid(True)
    plt.savefig(f"Graphs/FrequencyDomainLog/{title}.png")
    print(f"Frequency domain graph for {title} saved successfully to Graphs/FrequencyDomainLog/")
    return


# Normalises all of an array's values to be from -1 to 1
def normalise(array):
    return array/np.max(array)


# Finds and returns the fundamental frequency + first x number_of_overtones after the fundamental frequency, by searching
# for a local maximum within +- fundamental_frequency*search_window_coefficient of eac approximate overtone location
def find_x_overtones(number_of_overtones, magnitude_spectrum, total_samples, expected_fundamental_frequency, sample_rate=44100, search_window_coefficient=0.2):

    overtones = []

    # Converting to proper array index and finding a more precise fundamental frequency peak index within the window around original estimate
    fundamental_frequency_index = expected_fundamental_frequency*total_samples/sample_rate
    window_start, window_end = int(fundamental_frequency_index-fundamental_frequency_index*0.2), int(fundamental_frequency_index+fundamental_frequency_index*0.2)
    fundamental_frequency_index = window_start + np.argmax(magnitude_spectrum[window_start:window_end])
    print("Nearest fundamental frequency to estimate found at:", fundamental_frequency_index*sample_rate/total_samples, "Proceeding to look for overtones from this point")
    overtones.append(magnitude_spectrum[fundamental_frequency_index])

    search_window_size = search_window_coefficient * fundamental_frequency_index

    if fundamental_frequency_index * (number_of_overtones + 2) > sample_rate / 2:
        print("The given number of overtones of this fundamental frequency cannot be represented at the current sample rate, please increase sample rate or decrease overtone count")
        return

    for current_overtone in range(2, number_of_overtones + 2):
        overtones.append(max(magnitude_spectrum[int(fundamental_frequency_index * current_overtone - search_window_size):
                                                int(fundamental_frequency_index * current_overtone + search_window_size)]))

    return overtones


def load_frequency_features(graph_type):
    data = np.array([])
    first_array = True

    print("Loading frequency peaks array data...\n")
    for file in os.listdir("OutputArrays/FrequencyPeaks"):
        if first_array:
            data = np.append(data, np.loadtxt(f"OutputArrays/FrequencyPeaks/{file}"))
            first_array = False
        else:
            temp_array = np.loadtxt(f"OutputArrays/FrequencyPeaks/{file}")
            data = np.vstack((data, temp_array))
    print("Vertical array size =", len(data), "Array contents:\n", data, "\n")
    return data

def generate_principal_component_graph(number_instruments, projected_data, instruments, explained_variance, graph_type):
    plt.figure(figsize=(12, 9))

    # Extract unique base names and assign colors
    unique_bases = set()
    for inst in instruments:
        if inst.startswith("Organ"):
            base = inst[5:]
        elif inst.startswith("Instrument"):
            base = inst[10:]
        else:
            base = inst  # Fallback for unexpected names
        unique_bases.add(base)

    # Assign colors from Matplotlib's default cycle
    color_dict = {base: f'C{idx}' for idx, base in enumerate(sorted(unique_bases))}

    # Plot each point with shape based on prefix and color based on base name
    for i in range(number_instruments):
        inst = instruments[i]
        if inst.startswith("Organ"):
            base = inst[5:]
            marker = '>'
        elif inst.startswith("Instrument"):
            base = inst[10:]
            marker = 'o'  # Default circle for instruments
        else:
            base = inst
            marker = 'x'  # Fallback marker

        color = color_dict.get(base, 'black')  # Fallback color
        plt.scatter(projected_data[i, 0], projected_data[i, 1], label=inst, marker=marker, color=color)


    plt.ylabel('Principal Component 2')
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.grid(True)
    plt.xlabel(f'Principal Component 1, significance level ≈ {explained_variance[0]:.3f}', fontsize=14)
    plt.ylabel(f'Principal Component 2, significance level ≈ {explained_variance[1]:.3f}', fontsize=14)
    if graph_type == "1":
        plt.title(f'Even Overtone Principal Component Analysis (PCA) Organ/Instruments Sample Pairs', fontsize=14, fontweight='bold')
        plt.savefig(f"Graphs/PCA/EvenPCAGraph.png", bbox_inches='tight')
    if graph_type == "2":
        plt.title(f'Odd Overtone Principal Component Analysis (PCA) Organ/Instruments Sample Pairs', fontsize=14, fontweight='bold')
        plt.savefig(f"Graphs/PCA/OddPCAGraph.png", bbox_inches='tight')
    if graph_type == "3":
        plt.title(f'Full Overtone Principal Component Analysis (PCA) Organ/Instruments Sample Pairs', fontsize=14, fontweight='bold')
        plt.savefig(f"Graphs/PCA/FullPCAGraph.png", bbox_inches='tight')
    print(f"Graph saved to Graphs/PCA/\n")
