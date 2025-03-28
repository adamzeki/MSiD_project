# MSiD_project
The script data_analysis_main generates a collection of images and information useful in the analysis of a dataset.
The analyze_write_data() function called within main is responsible for the computing, generation and saving the aforementioned statistics
on your device. It takes three parameters:

- **input_path** - the path to the csv file you want analyzed
- **output_path** - the path to the output csv file, where the text data will be saved
- **image_dir_path** - the path to the directory, where all the images will be saved

By default, output_path and image_dir_path will be created in your project directory