from flask import Blueprint, render_template, request, jsonify, flash, send_from_directory
from flask_login import login_required, current_user
from utils.model import predict_dataset, get_training_analytics, load_model
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
import plotly.utils
from flask import redirect, url_for

user_bp = Blueprint('user', __name__)

ALLOWED_EXT = {'npz'}

class TestUploadForm(FlaskForm):
    file = FileField('Test dataset (.npz)', validators=[
        FileRequired(),
        FileAllowed(['npz'], 'NPZ files only!')
    ])
    submit = SubmitField('Analyze')

@user_bp.route('/upload_test', methods=['GET', 'POST'])
@login_required
def upload_test():
    if current_user.role != 'user':
        flash('Access denied')
        return redirect(url_for('main.dashboard'))
    
    form = TestUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(filepath)
        
        try:
            preds, true, acc = predict_dataset(filepath)
            analytics = get_training_analytics()
            return render_template('user/analytics.html', 
                                 acc=acc, analytics=analytics,
                                 graphJSON1=analytics_graph1(analytics),
                                 graphJSON2=analytics_graph2(analytics),
                                 graphJSON3=analytics_graph3(analytics),
                                 graphJSON4=analytics_graph4(analytics))
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            os.remove(filepath)
    
    return render_template('user/upload.html', form=form)

def analytics_graph1(analytics):  # Accuracy vs epochs
    fig = go.Figure(data=go.Scatter(x=analytics['epochs'], y=analytics['accuracy'], mode='lines'))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def analytics_graph2(analytics):  # Train classes pie
    labels = list(analytics['train_classes'].keys())
    values = list(analytics['train_classes'].values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def analytics_graph3(analytics):  # Test accuracy per sample
    fig = px.histogram(x=range(len(analytics['test_acc'])), y=analytics['test_acc'])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def analytics_graph4(analytics):  # Top-5 valid
    fig = go.Bar(x=list(range(5)), y=analytics['valid_top5'])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
