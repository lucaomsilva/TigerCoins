# model_train.py

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.svm import SVR
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def treinar_modelo(X_train, y_train, algoritmo, tipo_saida='regressao', parametros=None):
    if parametros is None:
        parametros = {}
    # Choose model based on task type
    if tipo_saida == 'regressao':
        if algoritmo == "Regressão Linear":
            modelo = LinearRegression(**parametros)
        elif algoritmo == "Random Forest":
            modelo = RandomForestRegressor(**parametros)
        elif algoritmo == "KNN":
            modelo = KNeighborsRegressor(**parametros)
        elif algoritmo == "SVM":
            modelo = SVR(**parametros)
        elif algoritmo == "XGBoost":
            modelo = XGBRegressor(**parametros)
        else:
            raise ValueError("Algoritmo não suportado")
    else:  # classificacao
        if algoritmo == "Regressão Linear":
            modelo = LogisticRegression(**parametros)        # use logistic regression for classification
        elif algoritmo == "Random Forest":
            modelo = RandomForestClassifier(**parametros)
        elif algoritmo == "KNN":
            modelo = KNeighborsClassifier(**parametros)
        elif algoritmo == "SVM":
            modelo = SVC(**parametros)
        elif algoritmo == "XGBoost":
            modelo = XGBClassifier(use_label_encoder=False, eval_metric='logloss', **parametros)
        else:
            raise ValueError("Algoritmo não suportado")
    modelo.fit(X_train, y_train)
    return modelo

def prever_modelo(modelo, X_test):
    return modelo.predict(X_test)

def avaliar_modelo(y_true, y_pred, tipo_saida='regressao'):
    if tipo_saida == 'regressao':
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return {'MAE': mae, 'RMSE': rmse}
    else:
        accuracy = (np.array(y_pred) == np.array(y_true)).mean()
        return {'Accuracy': accuracy}
