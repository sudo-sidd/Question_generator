# import nltk
# import os

# # Set the local nltk_data path
# nltk_data_path = "/mnt/data/PROJECTS/Question_generator/nltk_data"
# os.makedirs(nltk_data_path, exist_ok=True)
# nltk.data.path.append(nltk_data_path)

# # Download punkt_tab and averaged_perceptron_tagger to the local folder
# nltk.download('punkt_tab', download_dir=nltk_data_path)
# nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_path)

# print("Resources downloaded to", nltk_data_path)

import nltk
nltk.download('averaged_perceptron_tagger_eng', download_dir='/mnt/data/PROJECTS/Question_generator/nltk_data')