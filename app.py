from flask import Flask, render_template, redirect, url_for, request, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired, Length
import numpy as np
import pickle
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C7HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

class NameForm(FlaskForm):
    nit=IntegerField('Nitrogen content',validators=[DataRequired()])
    phos=IntegerField('Phosphorus content',validators=[DataRequired()])
    pot=IntegerField('Potassium content',validators=[DataRequired()])
    temp=FloatField('Temperature',validators=[DataRequired()])
    hum=FloatField('Humidity',validators=[DataRequired()])
    ph=FloatField('PH level',validators=[DataRequired()])
    rain=FloatField('Average rainfall in mm',validators=[DataRequired()])
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
    acc=[0.990, 0.952, 0.981, 0.9, 0.963]
    algo=['RF','LR','SVM','SGD','KNN']
    RF_model=pickle.load(open('Model/RandomForest_Model.pkl', 'rb'))
    LR_model=pickle.load(open('Model/Logistic_Regression.pkl', 'rb'))
    SVM_model=pickle.load(open('Model/SVM.pkl', 'rb'))
    SGD_model=pickle.load(open('Model/SGD.pkl', 'rb'))
    KN_model=pickle.load(open('Model/Knearest.pkl', 'rb'))

    # fig = plt.figure(figsize = (10,6))
    # plt.bar(algo, acc, color ='green',width = 0.4)
    # plt.xlabel("Algorithm names", fontsize=20)
    # plt.ylabel("Accuracy", fontsize=20)
    # plt.title("Classification Algorithm", fontsize=25)
    # for index, value in enumerate(acc):
    #     plt.text(index,value, str("{:.3f}".format(value)))
    # plt.savefig('static/plot.png', dpi=300, bbox_inches='tight')


    
    if form.validate_on_submit():
        data = np.array([[form.nit.data,form.phos.data,form.pot.data,form.temp.data,form.hum.data,form.ph.data,form.rain.data]])
        prediction=RF_model.predict(data)
        msg1 = prediction[0].capitalize() 
        prediction=LR_model.predict(data)
        msg2 = prediction[0].capitalize() 
        prediction=SVM_model.predict(data)
        msg3 = prediction[0].capitalize() 
        prediction=SGD_model.predict(data)
        msg4 = prediction[0].capitalize() 
        prediction=KN_model.predict(data)
        msg5 = prediction[0].capitalize() 

        img1='../static/'+msg1+'.jpg'
        img2='../static/'+msg2+'.jpg'
        img3='../static/'+msg3+'.jpg'
        img4='../static/'+msg4+'.jpg'
        img5='../static/'+msg5+'.jpg'
        images=[img1,img2,img3,img4,img5]
        crop=['1.'+msg1,'2.'+msg2,'3.'+msg3,'4.'+msg4,'5.'+msg5]
        crop1=[msg1,msg2,msg3,msg4,msg5]
        create_figure(algo,acc)
        create_figure2(crop,acc)
        return render_template('result.html', form=form, img=images,crop=crop1)
    else:
        message = "Please check your input."
    return render_template('ind.html', form=form, message=message)

def create_figure(xs,ys):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(xs, ys,color ='green',width = 0.4)
    axis.set_xlabel("Algorithm names")
    axis.set_ylabel("Accuracy")
    axis.set_title("Classification Algorithm")
    for index, value in enumerate(ys):
        axis.text(index,value, str("{:.3f}".format(value)))
    fig.savefig('static/plotx.png', dpi=300, bbox_inches='tight')

def create_figure2(xs,ys):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(xs, ys,color ='green',width = 0.4)
    axis.set_xlabel("Crops name")
    axis.set_ylabel("Accuracy")
    axis.set_title("Crop Recommended")
    for index, value in enumerate(ys):
        axis.text(index,value, str("{:.3f}".format(value)))
    fig.savefig('static/ploty.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    app.run()