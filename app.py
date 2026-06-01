from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from model.predictor import predict as run_pre
from model.disease_info import DISEASE_INFO
from model.quality import check_image_quality

app=Flask(__name__)

UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath=os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
    file.save(filepath)

    #image quality
    is_good, quality_message = check_image_quality(filepath)
    if not is_good:
        return jsonify({'error': quality_message})

    #run prediction
    try:
        result=run_pre(filepath)
        condition = result['condition']
        info = DISEASE_INFO.get(condition, {})

        response = jsonify({
            'condition': condition,
            'confidence': result['confidence'],
            'description': info.get('description', ''),
            'severity': info.get('severity', ''),
            'symptoms': info.get('symptoms', []),
            'precautions': info.get('precautions', []),
            'consult_when': info.get('consult_when', ''),
            'disclaimer': 'This is not a medical diagnosis. Please consult a certified dermatologist.'
        })
        
        # Clean up uploaded file
        os.remove(filepath)
        return response
        
    except Exception as e :
        # Clean up file on error too
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error':str(e)})

    
if __name__=='__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
