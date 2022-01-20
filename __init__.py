from flask import Flask, render_template, redirect, url_for, request, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired, Length
import numpy as np
import pickle


app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C7HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

class NameForm(FlaskForm):
    nit=IntegerField('Nitrogen content',validators=[DataRequired()])
    phos=IntegerField('phosphorus content',validators=[DataRequired()])
    pot=IntegerField('Potassium content',validators=[DataRequired()])
    temp=FloatField('Temperature',validators=[DataRequired()])
    hum=FloatField('Humidity',validators=[DataRequired()])
    ph=FloatField('PH level',validators=[DataRequired()])
    rain=FloatField('Average Rainfall in mm',validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/crop', methods=['GET', 'POST'])
def index():
    form = NameForm()
    message = ""
    RF_model=pickle.load(open('Model/RandomForest_Model.pkl', 'rb'))
    LR_model=pickle.load(open('Model/Logistic_Regression.pkl', 'rb'))
    SVM_model=pickle.load(open('Model/SVM.pkl', 'rb'))
    SGD_model=pickle.load(open('Model/SGD.pkl', 'rb'))
    KN_model=pickle.load(open('Model/Knearest.pkl', 'rb'))

    if form.validate_on_submit():
        data = np.array([[form.nit.data,form.phos.data,form.pot.data,form.temp.data,form.hum.data,form.ph.data,form.rain.data]])
        prediction=RF_model.predict(data)
        msg1 = prediction[0]
        prediction=LR_model.predict(data)
        msg2 = prediction[0]
        prediction=SVM_model.predict(data)
        msg3 = prediction[0]
        prediction=SGD_model.predict(data)
        msg4 = prediction[0]
        prediction=KN_model.predict(data)
        msg5 = prediction[0]
        return render_template('result.html', form=form, msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5)
    else:
        message = "Please check your input."
    return render_template('ind.html', form=form, message=message)

if __name__ == '__main__':
    app.run()