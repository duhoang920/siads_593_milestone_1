# SIADS 593: Milestone I

This repository contains a modular Python data pipeline designed to load, clean, transform, analyze, and visualize structured datasets. The workflow is orchestrated through a Jupyter Notebook and supported by reusable Python modules for data loading, wrangling, and visualization.

## Project Structure

```
.
├── main.ipynb          # Orchestrates the end-to-end workflow
├── Data_loader.py      # Functions for loading and saving data
├── Data_wrangle.py     # Data cleaning, transformation, and processing logic
├── visual2.py          # Plot generation and visualization formatting
├── data/
│   ├── raw/            # Raw input datasets
│   └── processed/      # Cleaned and processed outputs
└── README.md

```
## File Descriptions
### main.ipynb - Orchestrator
The main notebook serves as a control center for the project.

* Imports fuctions from the supporting Python Modules.
* Loads raw datasets.
* Applies data cleaning and transformation steps.
* Merges processed datasets.
* Generates visualizations.

### data_loader.py - Data Loading & Saving
This module centralizes all inputs/output operations.

* Loading CSV files into pandas DataFrames.
* Saving processed DataFrames back to disk as a CSV file.

### data_wrangle.py - Data Cleaning & Transformation
This module contains the core data-processing logic.

* Adding, removing, and renaming columns.
* Filtering rows and columns based on criteria.
* Handleing missing values.
* Coverting data types.
* Data specific transformations.
* Merging and reshaping datasets for analysis.

### visual2.py - Visualization
This module is responsbile for all visual outputs.

* Creating histograms, boxplots, and correlation plots.
* Formatting visual elements for readability and consistency

## Typical Workflow
1. Run main.ipynb
2. Load raw data using functions from data_loader.py
3. Clean, transform, and merge data using data_wrangle.py
4. Save processed DataFrames using data_loader.py
5. Generate plots and visuals using visual2.py

## Dependencies
This project relies on common Python libraries.

* pandas
* numpy
* matplotlib
* seaborn
* jupyter