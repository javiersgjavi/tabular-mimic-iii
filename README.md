# Repository to generate tabular data from MIMIC-III dataset

This repository contains the data to generate the main dataset used in the article: [Comparing artificial intelligence strategies for early sepsis detection in the ICU: an experimental study](https://doi.org/10.1007/s10489-023-05124-z)

# Table of Contents
1. [Abstract](#Abstract) 
2. [Authors](#Authors) 
3. [Prerequisites](#Prerequisites)
4. [How to download and generate the base data](#Generate)
5. [What does the repository?](#What_Does)
6. [How to define the data to be generated?](#Define)
7. [How to launch the data generation?](#Launch)
8. [What format will the data be in?](#Data_format)
9. [How works the code of the repository?](#Code)
10. [License](#license) 

<a name="Abstract"/>

## Abstract

[Comparing artificial intelligence strategies for early sepsis detection in the ICU: an experimental study](https://doi.org/10.1007/s10489-023-05124-z)

> Sepsis is a life-threatening condition whose early recognition is key to improving outcomes for patients in intensive care units (ICUs). Artificial intelligence can play a crucial role in mining and exploiting health data for sepsis prediction. However, progress in this field has been impeded by a lack of comparability across studies. Some studies do not provide code, and each study independently processes a dataset with large numbers of missing values. Here, we present a comparative analysis of early sepsis prediction in the ICU by using machine learning (ML) algorithms and provide open-source code to the community to support future work. We reviewed the literature and conducted two phases of experiments. In the first phase, we analyzed five imputation strategies for handling missing data in a clinical dataset (which is often sampled irregularly and requires hand-crafted preprocessing steps). We used the MIMIC-III dataset, which includes more than 5,800 ICU hospital admissions from 2001 to 2012. In the second phase, we conducted an extensive experimental study using five ML methods and five popular deep learning models. We evaluated the performance of the methods by using the area under the precision-recall curve, a standard metric for clinical contexts. The deep learning methods (TCN and LSTM) outperformed the other methods, particularly in early detection tasks more than 4 hours before sepsis onset. The motivation for this work was to provide a benchmark framework for future research, thus enabling advancements in this field.


<a name="Authors"/>

## Authors:
- Javier Solís-García
- Belén Vega-Márquez
- Juan Nepomuceno
- José C. Riquelme-Santos
- Isabel A. Nepomuceno-Chamorro


<a name="Prerequisites"/>

## Prerequisites

This repository has been tested with the following requirements; however, it may be run with a different version of the listed software:

1. Ubuntu 20.04 or 22.04
2. Docker version 20.10.18
3. docker-compose version 1.29.2
4. Nvidia Container Tookit

<a name="Generate"/>

## How to download and generate the base data

### Clone the repository

The repository can be cloned with the command: ```git clone https://github.com/javiersgjavi/tabular-mimic-iii.git```

### Generate the base data

```Warning:``` This guide has been made for Ubuntu 20.04, it should be similar for other Linux versions, but may differ for a different operating system

#### Download data from PhysioNet and create PostgresSQL DB with the [MIT-LCP/mimic-code](https://github.com/MIT-LCP/mimic-code) repository

1. Request access to MIMIC-III data in [PhysioNet](https://mimic.mit.edu/docs/gettingstarted/).

2. Go to the folder _build_mimic_data_: ```cd build_mimic_data```.

3. Add your user of physionet with access privileges to MIMIC-III in line1 of file _download_physionet_data.sh_, where it says <User_of_physionet>.

4. Give execution permissions to all the .sh files with the following command: ```chmod +x *.sh```.

5. Execute the following command: ```sudo ./download_physionet_data.sh```. The process can be long and will require:

- Enter the password of your PhysioNet account to download the data.
- You will watch the log of the postgres database being loaded. You must wait until you see a table with the tables of the DB where all rows return "PASSED", and below must display the message "Done!" before going to the next steps.
- Once the process is finished, press: ```Ctrl + C``` to finish the display of the log.

#### Create CSV files from the PostgresSQL DB with the [BorgwardtLab/mgp-tcn](https://github.com/BorgwardtLab/mgp-tcn) repository
6. Execute the following command: ```./preprocess_data.sh```.
7. Give execution permissions _main.sh_ file with the command: ```chmod +x src/query/main.sh```.
8. Execute the command: ```make query```. This process will be longer than the one in the 6 step.

#### Create the final data with [BorgwardtLab/mgp-tcn](https://github.com/BorgwardtLab/mgp-tcn) repository
9. Execute the command: make generate_data to generate the final data that the repository will use.
10. Exit from the container with the command: ```exit```.
11. Execute the command: ```./create_data_folder.sh```.

<a name="What_Does"/>

## What does the repository?

This repository focuses in the generation of the data used in the paper. The motivation is to facilitate the generation of the data to allow an easy comparation in new researches. To archive this task, we will transform the data used in [BorgwardtLab/mgp-tcn](https://github.com/BorgwardtLab/mgp-tcn) to a tabular data, facilitating the use of MIMIC-III data, which is a irregular sampled database of UCI patients,


<a name="Define"/>

## How to define the data to be generated?

The characteristics of the data generation are defined in the file __main.py__.:

- **imputation_methods**: It is a dict with all available imputation methods, put 1 to activate an imputation method, or 0 to deactivate it.

<a name="Launch"/>

## How to launch the data generation?

- It is important to give execution permissions to the _start.sh__ file if it hasn't with the command: ```chmod +x start.sh```.

- Start and enter to the docker container with the command: ```./start.sh```. 

- Launch the experiment with the command: ```python main.py```. 

- If you want to execute in second plane, use the command: ```nohup python main.py```.

<a name="Data_format"/>
## What format will the data be in?

At the end of the execution, 3 folders will be generated, which will contain the train, val and test data, and inside each of them 3 independent files in .npy format:

- x_dl.npy: this file contains the data of each patient in 3 dimensions:
    - 1 dimension: contains the patients.
    - 2 dimension: contains the different measurements.
    - 3 dimension: contains the time instants from [-49h, 0h] being 0h the onset instant.

Thus, if we want to consult the measurement 4 of patient 2 at time instant -48, it would be consulted as follows:

```
import numpy as np
x = np.load('x_dl.npy')
print(x[2, 4, 1])
```

- x_ml.npy: This file contains the data of each patient but in 2 dimensions, so that it is easily applicable with machine learning models. To achieve this dimension reduction we simply applied numpy's .flatten() function, so ```x_ml = x_dl.flatten()```. This file contains a number of rows equal to the number of patients, and a number of columns equal to 2156(number_of_measures*hours_before_sepsis). The column distribution has been constructed by concatenating successively the 49h of each measurement, so the first 49 columns represent the columns of [-49h, 0h] of measurement 0, and so on for each of the measurements.

- y.npy: this file contains the classification of each patient, if the patient is positive it will be marked as 1, and 0 otherwise.

The measures used to detect the occurrence of sepsis can be seen in the following list:
```
0. sysbp
1. diabp
2. meanbp
3. resprate
4. heartrate
5. spo2_pulsoxy
6. tempc
7. cardiacoutput
8. tvset
9. tvobserved
10. tvspontaneous
11. peakinsppressure
12. totalpeeplevel
13. o2flow
14. fio2
15. albumin
16. bands
17. bicarbonate
18. bilirubin
19. creatinine
20. chloride
21. glucose
22. hematocrit
23. hemoglobin
24. lactate
25. platelet
26. potassium
27. ptt
28. inr
29. pt
30. sodium
31. bun
32. wbc
33. creatinekinase
34. ck_mb
35. fibrinogen
36. ldh
37. magnesium
38. calcium_free
39. po2_bloodgas
40. ph_bloodgas
41. pco2_bloodgas
42. so2_bloodgas
43. troponin_t
```
<a name="Code"/>

## How works the code of the repository?

- **main.py**: it is the script that generate the data.
- **utils/preprocess_data.py**: it is a script that contains all functions that preprocess the data. This script contains all functions to make the different imputations methods and probably is the more messy and difficult file to understand in this repository. I'm sorry for the untidy state of this file, but the management of the input data was very chaotic due to its format.
- **classes/DataGeneration.py**: is the class that read the previous data generated by [BorgwardtLab/Imputing_Signatures](https://github.com/BorgwardtLab/Imputing_Signatures) repository and manage the transfomation to the tabular data.
- **classes/MGP.py**: the code of this file implement de MGP used in the gaussian process imputation. All code in this file is extracted from [BorgwardtLab/Imputing_Signatures](https://github.com/BorgwardtLab/Imputing_Signatures) repository.
- **data**: this folder will be generated during the execution of the repository and will contain the original data and the imputed data to reduce the execution time.
- **build_mimic_data**: this folder is used to download and generate the data which will be used. It contains the clone of two repositories:
  - [MIT-LCP/mimic-code](https://github.com/MIT-LCP/mimic-code) repository: is used to download de MIMIC-III data from physionet
  - [BorgwardtLab/mgp-tcn](https://github.com/BorgwardtLab/mgp-tcn): is used to generate the data that will be used by the experiments.


## License<a name="license"></a>

This project is licensed under the BSD-3-Clause license - see the [LICENSE](LICENSE) file for details
