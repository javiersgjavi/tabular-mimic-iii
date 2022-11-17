import os

from classes.DataGeneration import DataGeneration



def main(imputation_methods):


    print('[INFO] STARTING DATA GENERATION')
    data_generation = DataGeneration(imputation_methods)
    data_generation.generate()

    print('[INFO] EXECUTION FINISHED')


if __name__=='__main__':
    
    # Mark the chosen ones with 1, others with 0

    imputation_methods = {
        'nan_imputation': 1,
        'carry_forward': 1,
        'forward_filling': 1,
        'zero_imputation': 1,
        'gaussian_process': 1,
        'linear_interpolation': 1,
        'indicator_imputation': 1,
        }
    

    main(imputation_methods)