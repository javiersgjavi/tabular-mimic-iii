import pickle

from utils.preprocess_data import preprocess_general, preprocess_gp

class DataGeneration:
    def __init__(self, imputation_methods):

        self.data_original_path='./data/original/'

        self.imputation_methods = []
        for method in imputation_methods.keys():
            if imputation_methods[method] == 1:
                self.imputation_methods.append(method)


    def _generate_data(self, imputation_method):
        print(f'Loading data with imputation method: {imputation_method}')

        with open(f'{self.data_original_path}train_data.pkl', 'rb') as f:
            train_data = pickle.load(f)

        with open(f'{self.data_original_path}val_data.pkl', 'rb') as f:
            val_data = pickle.load(f)

        with open(f'{self.data_original_path}test_data.pkl', 'rb') as f:
            test_data = pickle.load(f)

        # Preprocess data with chosen imputation method
        if imputation_method == 'gaussian_process':
            preprocess_gp(train_data, val_data, test_data) 

        else:
            preprocess_general(train_data, val_data, test_data, imputation_method)
        

    def generate(self):

        for imputation_method in self.imputation_methods:
           self._generate_data(imputation_method)

            