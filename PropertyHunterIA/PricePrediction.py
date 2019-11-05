import pandas as pd  
import numpy as np 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV


def getOfferPrice(projectname, district, area, floor):
    print(projectname)
    print(district)
    print(area)
    print(floor)
    dataset = pd.read_csv("merged_data.csv")
    dataset = dataset.drop(['Street Name','Market Segment','Tenure','Type of Sale','Price ($)','No. of Units','Nett Price ($)','Type of Area','Type','Unit Price ($psf)','Date of Sale'], axis=1)
    
    multiplier_data = pd.read_csv("future_price_multiplier.csv")
    multiplier = multiplier_data['Multiplier'][0]

    level = ""

    if floor in ('Ground Floor','Low Floor'):
        level = "01 to 05"
    elif floor in ('Middle Floor'):
        level = "06 to 10"
    elif floor in ('High Floor','Penthouse'):
        level = "10 to 15"
    else:
        level = "06 to 10"

    data = dataset[dataset['Project Name']==projectname]

    if len(data) < 10:
        data = dataset[dataset['Postal District']==district]

    data = data.drop(['Postal District','Project Name'],axis=1)    

    floor_data = data[data['Floor Level']==level]

    if len(floor_data) > 0:
        df = pd.DataFrame([[area,level]], columns = ['Area (Sqft)', 'Floor Level'])
        data = pd.concat([df, data], axis=0, sort=False)
        data['Floor Level'] = pd.Categorical(data['Floor Level'])
        dfDummies = pd.get_dummies(data['Floor Level'], prefix = 'floor_level')
        data = pd.concat([data, dfDummies], axis=1)
        query = data[0:1]
        query = query.drop(['Floor Level','Present Value'],axis=1)
        data = data[1:]
        y = data['Present Value'].values
    else:
        query = pd.DataFrame([[area]], columns = ['Area (Sqft)'])
        y = data['Present Value'].values

    X = data.drop(['Floor Level','Present Value'],axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    param_grid = {
        'criterion':['mse','mae'],
        'max_depth':[4,8,None],
        'min_samples_leaf':[1,2,3]
    }

    regr = RandomForestRegressor(max_depth=7, random_state=0, n_estimators=100)
    regr.fit(X_train, y_train)

    return int(regr.predict([query.iloc[0,:].values])* multiplier)

