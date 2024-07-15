# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np

# Flask constructor takes the name of 
# current module (__name__) as argument.
app2 = Flask(__name__ )
model = pickle.load(open('housePredictionLinearModel.pkl' , 'rb'))
data = pd.read_excel(r'HousePricePrediction.xlsx')


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app2.route('/')
# ‘/’ URL is bound with hello_world() function.


def index():
    BldgType = data['BldgType'].unique()
    OverallCond	 = sorted(data['OverallCond'].unique())
    YearBuilt = sorted(data['YearBuilt'].unique() , reverse=True)
    YearRemodAdd = sorted(data['YearRemodAdd'].unique() , reverse=True)
    print(BldgType)

    
    return render_template('index.html' , BldgType = BldgType , OverallCond	 = OverallCond	 , YearBuilt = YearBuilt , YearRemodAdd =  YearRemodAdd)
    
    
@app2.route('/predict' , methods = ['POST'])
@cross_origin()
def predict():
    lotArea = request.form.get('area_plot')
    bldgType = request.form.get('type')
    overallCond = request.form.get('condition')
    yearBuilt = request.form.get('year_built')
    yearRemod = request.form.get('year_renov')
    totalbsmtarea = request.form.get('area_base')

    prediction=model.predict(pd.DataFrame(columns=[ 'Id', 'LotArea', 'BldgType', 'OverallCond', 'YearBuilt', 'YearRemodAdd' , 'TotalBsmtSF'],
                              data=np.array([1,lotArea,bldgType,overallCond,yearBuilt,yearRemod,totalbsmtarea ]).reshape(1, 7)))
    
    return str(np.round(prediction[0] , 2))


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app2.debug = True;
    app2.run()
