import os

# Deletes all current contents of the output folders including graphs and arrays
def reset_output_folder(folder_clean_path):
    for filename in os.listdir(folder_clean_path):
        file_path = os.path.join(folder_clean_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)