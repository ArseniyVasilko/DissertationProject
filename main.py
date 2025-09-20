import os
from modules.extract_audio_info import extractAudioInfo
from modules.pca_analysis import generate_pca_graph
from modules.reset import reset_output_folder


def main():


    while True:
        print("Please select an operation")
        print("1. Extract audio info from all files in the InputAudio folder")
        print("2. Generate PCA graphs based on array in the OutputArrays folder")
        print("3. Clear the array and graph output folders (full reset)")
        print("4. Exit")

        choice = input("Enter your choice (1-4): \n")

        match choice:
            case '1':
                print("Select the subfolder to take files from")
                print("1. Instrument")
                print("2. Organ")
                print("3. Go back")
                choice2 = input("Enter your choice (1-3): \n")
                match choice2:
                    case '1':
                        print("Instrument folder chosen")
                        while True:
                            print("Please type in the expected fundamental frequency of all audio files to be extracted."
                                  "The frequency must apply to all files in the folder and be reasonably accurate.")
                            expected_frequency = input()
                            try:
                                expected_frequency = int(expected_frequency)
                                break
                            except ValueError:
                                print("Fundamental frequency value must be an integer.\n")
                                pass
                        for filename in os.listdir("InputAudio/Instrument"):
                            extractAudioInfo(title=filename, folder_name="Instrument", expected_frequency=expected_frequency)
                    case '2':
                        print(">>Organ folder chosen\n")
                        while True:
                            print("Please type in the expected fundamental frequency of all audio files to be extracted."
                                  "The frequency must apply to all files in the folder and be reasonably accurate.\n")
                            expected_frequency = input()
                            try:
                                expected_frequency = int(expected_frequency)
                                break
                            except ValueError:
                                print("Fundamental frequency value must be an integer.\n")
                                pass
                        for filename in os.listdir("InputAudio/Organ"):
                            extractAudioInfo(title=filename, folder_name="Organ", expected_frequency=expected_frequency)
                    case '3':
                        print("Going back to main menu\n")
                    case _:
                        print("Invalid choice. Going back to main menu\n")

            case '2':
                while True:
                    graph_type = str(input("1.Even overtone PCA\n"
                                       "2.Odd overtone PCA\n"
                                       "3.Full overtone PCA\n"))

                    if graph_type != "1" and graph_type != "2" and graph_type != "3":
                        print("Invalid choice. Going back to main menu\n")
                        break

                    generate_pca_graph(graph_type=graph_type)
                    break

            case '3':
                if str(input("Are you sure? All the current file in the output folders will be deleted permanently y/N\n:")).lower() == "y":
                    reset_output_folder("Graphs/FrequencyDomain")
                    reset_output_folder("Graphs/FrequencyDomainLog")
                    reset_output_folder("Graphs/TimeDomain")
                    reset_output_folder("Graphs/PCA")
                    reset_output_folder("OutputArrays/FrequencyPeaks")
                    print("All output folders cleaned successfully\n")
                else:
                    print(">>Negative confirmation, going back to the main menu\n")

            case '4':
                print(">>Exiting...")
                break
            case _:
                print(">>Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
