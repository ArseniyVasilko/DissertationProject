import numpy as np
import os
import modules.functions as functions

def generate_pca_graph(graph_type):
    if os.listdir("OutputArrays/FrequencyPeaks") == []:
        print("No files available for pca analysis, please try again with frequency array files saved at OutputArrays/FrequencyPeaks\n")
        return
    # Loading frequency feature arrays from the OutputArrays folder
    data = functions.load_frequency_features(graph_type=graph_type)
    number_instruments = len(data)
    if graph_type == "2":
        first_array = True
        temp_data = np.array([])
        for array in data:
            if first_array:
                temp_data = np.append(temp_data, np.delete(array, np.arange(0, len(array), 2)))
                first_array = False
            else:
                temp_data = np.vstack((temp_data, np.delete(array, np.arange(0, len(array), 2))))
        data = temp_data

    elif graph_type == "1":
        first_array = True
        temp_data = np.array([])
        for array in data:
            if first_array:
                temp_data = np.append(temp_data, np.delete(array, np.arange(1, len(array), 2)))
                first_array = False
            else:
                temp_data = np.vstack((temp_data, np.delete(array, np.arange(1, len(array), 2))))
        data = temp_data
    print("after", data)
    # Creating labels for instruments
    instruments = [f"{file}"[:-9] for file in os.listdir("OutputArrays/FrequencyPeaks")]
    print("Instrument names being analysed:", instruments, "\n")

    # Standardising the data (mean center)
    mean = np.mean(data, axis=0)
    standard_deviation = np.std(data, axis=0)
    standardized_data = (data - mean) / standard_deviation

    # Computing covariance matrix
    covariance_matrix = np.cov(standardized_data.T)
    print("Covariance matrix:\n", covariance_matrix, "\n")

    # Computing eigenvalues and eigenvectors

    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Sorting eigenvalues and eigenvectors
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    # Selecting top 2 principal components for visualisation
    principal_components_num = 10
    principal_components = sorted_eigenvectors[:, :principal_components_num]

    # Projecting data onto principal components (matrix multiplication)
    projected_data = standardized_data @ principal_components

    # Explained variance printed
    explained_variance = sorted_eigenvalues / np.sum(sorted_eigenvalues)
    print("\nExplained Variance Ratio:")
    print(explained_variance[:principal_components_num])

    # Saving a graph of PCA results
    functions.generate_principal_component_graph(number_instruments=number_instruments,
                                                 projected_data=projected_data,
                                                 instruments=instruments,
                                                 explained_variance=explained_variance,
                                                 graph_type=graph_type)

