from sklearn.ensemble import IsolationForest
import pickle
import shap
import cloudpickle
import numpy as np


def load_models(isolation_forest_path='isolation_forest_model.pkl', pickle_file_path='exp.pkl'):
    with open(isolation_forest_path, 'rb') as file:
        iso_forest = pickle.load(file)
        
    #wczytaj shap
    #with open(pickle_file_path, 'rb') as file2:
    #   exp = pickle.load(file2)
    
    return iso_forest
        
def predict_and_get_cols(ROW, isolation_forest_path='model/iso_model.pkl'):

    iso_forest = load_models(isolation_forest_path)    
    #wybranie kolumn do predict
    # ROW = ROW.drop(columns = ['Unnamed: 0'])
    row_small = ROW.drop(columns = ['description', 'preprocessed_description', 'index',
           'possible_email', 'possible_address', 
           'possible_phone_numbers',
            'link',
           'dodane-data', 'id', 'title', 'category-tree-item', 'user-profile-link',
           'filters', 'pay_low', 'pay_high', 'pay_currency', 'pay_period',
           'Lokalizacja', 'Wymiar pracy', 'Typ umowy','user-profile-link-hash'])
    #predict
    #print(row_small.columns)
    iso_forest_pred = iso_forest.predict(row_small)

    #dodanie kolumny predict
    ROW['Predict_Flag'] = iso_forest_pred


    #dodanie explain
    exp = shap.TreeExplainer(iso_forest)
    shap_values1 = exp.shap_values(row_small.iloc[0,:])
    pr = np.mean(shap_values1)
    if pr <0.18:
        pr = (abs(pr-0.18))
    else:
        pr = 0
        
    if pr>1:
        pr=1
    ROW['Predict_Prob'] = pr
    
    cols = np.where(shap_values1<0)
    string = 'Odstaje od danych bo: '
    for col in cols:
        val = row_small.iloc[0, col][0]
        c = row_small.columns[col][0]
        string += f'{c} : {val}, '

    # Remove the trailing comma
    string = string.rstrip(', ')

    ROW['Explain'] = string
    return ROW