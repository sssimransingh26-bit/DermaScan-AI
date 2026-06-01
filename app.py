from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from model.predictor import predict as run_pre
from model.disease_info import DISEASE_INFO
from model.quality import check_image_quality

app=Flask(__name__)

UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error':'no file uploaded'})
    
    file=request.files['file']

    if file.filename=='':
        return jsonify({'error':'no file selected'})
    
    #save uploaded image
    filepath=os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
    file.save(filepath)

    #image quality
    is_good, quality_message = check_image_quality(filepath)
    if not is_good:
        return jsonify({'error': quality_message})

    #run prediction
    result=run_pre(filepath)
    condition = result['condition']
    info = DISEASE_INFO.get(condition, {})

    return jsonify({
        'condition': condition,
        'confidence': result['confidence'],
        'description': info.get('description', ''),
        'severity': info.get('severity', ''),
        'symptoms': info.get('symptoms', []),
        'precautions': info.get('precautions', []),
        'consult_when': info.get('consult_when', ''),
        'disclaimer': 'This is not a medical diagnosis. Please consult a certified dermatologist.'
    })

    
if __name__=='__main__':
   app.run(debug=True)