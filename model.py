from sklearn.ensemble import IsolationForest
import pickle
import shap

def load_models(isolation_forest_path='isolation_forest_model.pkl', pickle_file_path='exp.pickle'):
    with open(isolation_forest_path, 'rb') as file:
        iso_forest = pickle.load(file)
        
    #wczytaj shap
    with open(pickle_file_path, 'rb') as file:
        exp = pickle.load(file)
    
    return iso_forest, exp
        
def predict_and_get_cols(ROW, isolation_forest_path='isolation_forest_model.pkl', pickle_file_path='exp.pickle'):

    iso_forest, exp = load_models(isolation_forest_path, pickle_file_path)    
    #wybranie kolumn do predict
    ROW = ROW.drop(columns = ['Unnamed: 0'])
    row_small = ROW.drop(columns = ['description', 'preprocessed_description', 'index',
           'possible_email', 'possible_address', 
           'possible_phone_numbers',
            'link',
           'dodane-data', 'id', 'title', 'category-tree-item', 'user-profile-link',
           'filters', 'pay_low', 'pay_high', 'pay_currency', 'pay_period',
           'Lokalizacja', 'Wymiar pracy', 'Typ umowy'])
    #predict
    iso_forest_pred = iso_forest.predict(row_small)

    #dodanie kolumny predict
    ROW['Predict_Flag'] = iso_forest_pred


    #dodanie explain
    shap_values1 = exp.shap_values(row_small.iloc[0,:])

    ROW['Predict_Prob'] = np.mean(shap_values1)

    cols = np.where(shap_values1<0)
    string = 'Odstaje od danych bo: '
    for col in cols:
        val = X.iloc[0, col][0]
        c = X.columns[col][0]
        string += f'{c} : {val}, '

    # Remove the trailing comma
    string = string.rstrip(', ')

    ROW['Explain'] = string
    return ROW