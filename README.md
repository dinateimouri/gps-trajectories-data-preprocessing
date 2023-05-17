# GPS-Trajectories-Data-Preprocessing-And-Cleaning
This repository contains a workflow for processing GPS trajectories and segmenting the raw trajectories into individual trips taken by different users. The project focuses on the Geolife dataset, which is a widely used GPS trajectory dataset. More information about the Geolife dataset can be found on its official website: [Geolife Dataset](https://www.microsoft.com/en-us/research/publication/geolife-gps-trajectory-dataset-user-guide/).
The data_acquisition.py module provides functions to read PLT files, parse labels, and apply labels to the corresponding data points.
The data_preprocessing.py module performs necessary preprocessing and cleaning tasks on the data as well as segmenting to the individual trips. 
multithreading.py module is utilized to accelerate the processing of multiple labeled CSV files simultaneously. 
The main control flow and execution are managed in the main.py file.

For more details on the research behind this code, check out my thesis [here](https://lnkd.in/diu_Y9sp).
