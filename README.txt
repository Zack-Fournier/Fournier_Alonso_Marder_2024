The following code performs the simulations and analyses described in,


Zachary Fournier, Leandro M. Alonso, and Eve Marder, "Circuit function is more robust to changes in synaptic than intrinsic conductances", (2024)


**********
OVERVIEW:
**********

The model is implemented in java, and simulations and analyses are implemented in Python. The java code must be compiled into a .jar file. The python scripts call the .jar file to simulate the models and return their solutions.
IMPORTANT: To run each script, you must set the absolute path to the 'code_package' folder as the 'root_folder' at the top of each executable python script (i.e. 'C:/code_package')

*************
REQUIREMENTS
*************

- You need a java development kit to compile the code. (javaSDK https://www.oracle.com/technetwork/java/javase/downloads/index.html) 
java comes installed by default in many operating systems. 
To check if you have a running java and javac open a terminal and type 

> java -version

and 

> javac -version

- python 2.7 or newer. matplotlib, numpy, pandas, scipy, seaborn, scikit-learn (1.2.2) (anaconda recommended)

NOTE: to install scikit-learn use version 1.2.2 (i.e. 'pip install scikit-learn==1.2.2'), otherwise the scripts might not run

*************
COMPILE CODE
*************

To compile code, run the script 'compilejava.py' using an IDE or by running 'python compilejava.py' from the command line in the root folder (the location of the 'code_package' folder)


*************************************************
QUICK instructions to simulate a sample model
*************************************************

1) open the 'sample_model.py' script from the 'sample' folder

2) at the top of the script, enter the location of the root folder on your computer (the location of the 'code_package' folder) and save

3) run script


***************************
Overview of python scripts
***************************


There are 12 main scripts:


- Sensitivity_Analysis.py
- plot_curves.py
- full_SA_allmodels.py
- analysis_pipeline_cal.py
- ranges_specified_MP.py
- range_plot_figures_comparison.py
- MD_figure.py
- MD_features.py
- SA_average_plots.py
- sigmoidal_fit_analysis.py
- PCA_curves.py
- sample_traces.py


There are 10 supplementary scripts:


- ancillary_functions.py
- auxFunctions_plot.py
- classifyTraces.py
- colormap.py
- getCurrents.py
- integrate_and_plot_pyloric_imi_temp.py
- integratePyloricSQ10s_currentscapes_RK4_mp.py
- plotCurrentsTraces_rk4.py
- plotPyloricTempUtils.py
- pyloricMeasures.py



*************************
Guide to run all scripts
*************************

NOTE: main scripts need to be edited to set the root folder destination, whereas the supplementary scripts should not be edited or removed. Main scripts run the analyses and create figures, and the supplementary scripts contain functions used in the main scripts.


- Sensitivity_Analysis.py

	runs the sensitivity analysis for a single model of your choosing. consult the 'models' folder to choose the model you'd like to analyze, and input the name at the appropriate line at the top of the script. n=# of trials that the model is sampled for a given window size/delta value, n=1000 was used in this work but n=100 is recommended for a quick survey of the code. plots of each solution will be located in the 'plots' subfolders, and plots of the conductance distributions in the 'conductances_plots' subfolders; both of which are located in the 'IC_results'(intrinsic) and 'SC_results'(synaptic) subfolders in a folder titled as the model's name, which is located in the main folder 'SA'. Alter name of analysis folder if running numerous analyses on the same model.

- plot_curves.py

	plots the intrinsic and synaptic sensitivity curves for a single sensitivity analysis on a given model. input the name of the model used in the sensitivity analysis, as well as the value of n (number of trials)

- full_SA_allmodels.py

	runs the sensitivity analysis on all 100 models in the database. set number of trials (less than 1000 trials is not recommended if you're looking for a trustworthy result). WARNING: Do not attempt to run this code on a laptop computer, running on a computer cluster or gaming PC is recommended.

- analysis_pipeline_cal.py

	analyzes all of the models and extracts sensitivity curves. if the sensitivity analysis has been performed on all models, the plot from figure 4 can be created.

- ranges_specified_MP.py

	analyzes conductances ranges shown in this work for a chosen model.

- range_plot_figures_comparison.py


	plots conductance ranges shown in this work for a chosen model.

- MD_figure.py

	plots figure 2 from the paper.

- MD_features.py

	calculates features for all models in the database.

- SA_average_plots.py

	plots the average curves (fig. 5A) and area under the curves (fig. 5E) subplots in figure 5.

- sigmoidal_fit_analysis.py

	performs the sigmoidal fit analysis and produces the related subplots in figure 5B-D.

- PCA_curves.py

	performs PCA on curves and produces plot in figure 5F.

- sample_traces.py

	produces sample plots in figure 1C-F.



********
FOLDERS
********

There are 10 main folders:

- sample
- python
- java
- initial_conditions_and_parameters
- models
- SA
- analytics
- DATA
- range_data
- model_solutions
- MD_solutions


Guide to folder uses: 

- sample

	contains a script for running a sample model with a sample extraction of features

- python

	contains all python scripts

- java

	contains all java scripts

- intial_conditions_and_parameters

	contains initial conditions, starting parameters, and auxiliary solution files

- models

	contains parameter lists for all models used in this work

- analytics

	contains curve data, feature data, and a list of statistics relevant to the figures

- SA

	initially empty; will hold associated files for each sensitivity analysis run

- DATA

	initially empty; will hold the sensitivity analyses performed by the full_SA_allmodels.py script

- range_data

	initially empty; will hold the range data for each analysis performed

- model_solutions

	initially empty; will hold .txt files of the solutions for each model in the database if the MD_features.py script is run










