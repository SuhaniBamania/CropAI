import os
import uuid
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, make_response, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
from PIL import UnidentifiedImageError


# Import the new pest risk engine
from pest_risk import get_pest_risk_assessment, PestRiskEngine


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['WEATHER_API_KEY'] = None  # Add your OpenWeatherMap API key here if you have one
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Load the trained model once at startup
model = tf.keras.models.load_model('leaf_model_with_unknown.h5')
classes = ['Blight', 'Healthy', 'Mosaic', 'Rust', 'Unknown']  # Added "Unknown"
CONFIDENCE_THRESHOLD = 0.4  # Confidence below this => Unknown


# Your existing RECOMMENDATIONS dictionary stays the same
RECOMMENDATIONS = {
    'Blight': {
        'disease': 'Leaf Blight',
        'severity': 'High',
        'immediate_actions': [
            '🚨 Remove and destroy affected leaves immediately',
            '💧 Reduce watering frequency - avoid overhead watering',
            '🌿 Apply copper-based fungicide spray every 7-10 days',
            '🍃 Improve air circulation around plants'
        ],
        'preventive_measures': [
            '🌱 Plant resistant varieties in future seasons',
            '💨 Ensure proper plant spacing for air circulation',
            '🚰 Use drip irrigation instead of sprinkler systems',
            '🧹 Clean garden tools between plants'
        ],
        'monitoring': [
            '👁️ Check plants daily for new spots',
            '📊 Monitor humidity levels (keep below 85%)',
            '🌡️ Optimal temperature range: 20-25°C'
        ],
        'fertilizer_advice': 'Reduce nitrogen fertilizer temporarily. Apply balanced NPK (10-10-10) after disease control.',
        'organic_solutions': [
            '🥛 Spray diluted milk solution (1:10 ratio)',
            '🧄 Neem oil application every 5-7 days',
            '🍃 Baking soda spray (1 tsp per liter water)'
        ]
    },
    
    'Healthy': {
        'disease': 'No Disease Detected',
        'severity': 'None',
        'immediate_actions': [
            '✅ Continue current care routine',
            '💧 Maintain regular watering schedule',
            '🌿 Monitor for any changes in leaf color or texture'
        ],
        'preventive_measures': [
            '🔄 Rotate crops annually to prevent soil depletion',
            '🌱 Apply organic compost monthly',
            '🛡️ Maintain preventive spray schedule with neem oil',
            '🌾 Ensure proper plant nutrition'
        ],
        'monitoring': [
            '📅 Weekly health inspections',
            '🌧️ Monitor weather conditions for disease risks',
            '🐛 Check for early pest signs'
        ],
        'fertilizer_advice': 'Apply balanced fertilizer (NPK 20-20-20) bi-weekly during growing season.',
        'organic_solutions': [
            '🍂 Mulch around plants to retain moisture',
            '🦋 Encourage beneficial insects with companion planting',
            '☀️ Ensure 6-8 hours of direct sunlight daily'
        ]
    },
    
    'Mosaic': {
        'disease': 'Mosaic Virus',
        'severity': 'High',
        'immediate_actions': [
            '🚨 Isolate affected plants immediately',
            '🔥 Remove and burn infected plants (do not compost)',
            '🧤 Disinfect tools with 10% bleach solution',
            '🚫 Avoid handling healthy plants after touching infected ones'
        ],
        'preventive_measures': [
            '🐛 Control aphids and other virus-carrying insects',
            '🌱 Use certified virus-free seeds and seedlings',
            '🧹 Maintain strict garden hygiene',
            '🚰 Avoid overhead watering'
        ],
        'monitoring': [
            '🔍 Inspect new growth for mosaic patterns',
            '🐜 Monitor for aphid populations',
            '📈 Track spread to neighboring plants'
        ],
        'fertilizer_advice': 'Boost plant immunity with phosphorus-rich fertilizer. Avoid high nitrogen during infection.',
        'organic_solutions': [
            '🌿 Spray insecticidal soap for aphid control',
            '🧄 Apply neem oil to deter virus vectors',
            '🍃 Use reflective mulch to confuse aphids'
        ]
    },
    
    'Rust': {
        'disease': 'Leaf Rust',
        'severity': 'Medium',
        'immediate_actions': [
            '🍃 Remove rust-infected leaves and dispose in trash',
            '💨 Improve air circulation around plants',
            '🌿 Apply sulfur-based fungicide spray',
            '💧 Water at soil level, avoid wetting leaves'
        ],
        'preventive_measures': [
            '🌱 Choose rust-resistant plant varieties',
            '📏 Maintain proper plant spacing',
            '🌤️ Avoid watering in evening hours',
            '🧹 Clean up fallen leaves regularly'
        ],
        'monitoring': [
            '👀 Check undersides of leaves for orange spores',
            '🌡️ Monitor temperature (rust thrives in 20-25°C)',
            '💧 Watch humidity levels (high humidity increases risk)'
        ],
        'fertilizer_advice': 'Apply potassium-rich fertilizer to strengthen plant resistance. Reduce nitrogen temporarily.',
        'organic_solutions': [
            '🧄 Weekly neem oil applications',
            '☕ Spray compost tea to boost plant immunity',
            '🌿 Plant garlic nearby as natural fungicide'
        ]
    },
    
    'Unknown': {
        'disease': 'Unidentified Condition', 
        'severity': 'Unknown',
        'immediate_actions': [
            '📸 Take clearer photos with better lighting',
            '🔍 Consult agricultural expert for identification',
            '🌿 Isolate plant as precautionary measure'
        ],
        'preventive_measures': ['Not applicable until proper identification'],
        'monitoring': ['Not applicable until proper identification'], 
        'fertilizer_advice': 'Not applicable - proper diagnosis required first',
        'organic_solutions': ['Not applicable until proper identification']
    }
}

def get_comprehensive_recommendation(prediction, confidence_score=None):
    """
    Generate comprehensive recommendations based on disease prediction
    """
    base_rec = RECOMMENDATIONS.get(prediction, RECOMMENDATIONS['Unknown'])
    
    # Add confidence-based adjustments
    if confidence_score:
        if confidence_score < 0.6:
            base_rec = dict(base_rec)  # Create a copy
            base_rec['confidence_note'] = f'⚠️ Detection confidence: {confidence_score:.1%}. Consider getting second opinion.'
    
    return base_rec


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']


# NAVIGATION ROUTES - NEW ROUTES FOR MISSING TEMPLATES

@app.route('/')
def landing():
    """Root route - Landing page (first page users see)"""
    return render_template('landing.html')

@app.route('/soil-condition-card')
def soil_analysis():
    """Soil condition analysis page"""
    return render_template('soil-condition-card.html')

@app.route('/crop-report')
def crop_report():
    return render_template('crop-report.html')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/recommendation/<crop>')
def recommendation_detail(crop):
    # Add logic to handle individual crop recommendations
    # For now, you can return a simple template or redirect
    valid_crops = ['wheat', 'rice', 'maize']
    if crop.lower() in valid_crops:
        # You would typically pass crop-specific data here
        return render_template('recommendations.html', crop=crop)
    else:
        return redirect('/recommendations')


@app.route('/home')
def home():
    """Home page - redirects to landing page"""
    return render_template('landing.html')


@app.route('/features')
def features():
    """Features page - shows available features with cards"""
    return render_template('features.html')


@app.route('/about')
def about():
    """About page - information about the application"""
    return render_template('about.html')


@app.route('/chatbot')
def chatbot():
    """Chatbot support page"""
    return render_template('chatbot.html')


@app.route('/helpline')
def helpline():
    """Helpline & Government Resources page"""
    return render_template('helpline.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    response = make_response(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# NEW ROUTE: Pest Risk API endpoint
@app.route('/api/pest-risk')
def get_pest_risk():
    """API endpoint to get current pest risk assessment"""
    try:
        location = request.args.get('location', 'Delhi')
        assessment = get_pest_risk_assessment(location, app.config['WEATHER_API_KEY'])
        
        return jsonify({
            'success': True,
            'risk_level': assessment.risk_level,
            'risk_color': assessment.risk_color,
            'risk_emoji': assessment.risk_emoji,
            'confidence': assessment.confidence,
            'primary_threats': assessment.primary_threats,
            'recommendations': assessment.recommendations,
            'weather_summary': assessment.weather_summary,
            'detailed_analysis': assessment.detailed_analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'risk_level': 'Unknown',
            'risk_color': 'gray',
            'risk_emoji': '❓'
        }), 500



# NEW ROUTE: Dashboard page
@app.route('/dashboard')
def dashboard():
    """Dashboard page with pest risk indicator"""
    try:
        # Get pest risk assessment
        pest_assessment = get_pest_risk_assessment(api_key=app.config['WEATHER_API_KEY'])
        return render_template('dashboard.html', pest_risk=pest_assessment)
    except Exception as e:
        # Fallback if pest risk fails
        return render_template('dashboard.html', pest_risk=None, error=str(e))



@app.route('/index', methods=['GET', 'POST'])
def plant_detection():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return "No file part in the request.", 400
            
            f = request.files['file']
            if f.filename == '':
                return "No file selected. Please upload an image.", 400


            ext = ''
            if '.' in f.filename:
                ext = '.' + f.filename.rsplit('.', 1)[1].lower()
            else:
                ext = '.jpg'  # default extension if none provided


            if not allowed_file(f.filename):
                return "Unsupported file format. Please upload JPG or PNG image.", 400


            filename = f"upload_{uuid.uuid4().hex}{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)


            f.save(filepath)
            if os.path.getsize(filepath) < 1 * 1024:  # allow small but valid files
                os.remove(filepath)
                return "File too small or corrupted. Please upload a valid image.", 400


            img = image.load_img(filepath, target_size=(128, 128))
            img_array = image.img_to_array(img) / 255.0
            img_array = tf.expand_dims(img_array, axis=0)


            pred = model.predict(img_array)
            max_prob = tf.reduce_max(pred[0]).numpy()


            if max_prob < CONFIDENCE_THRESHOLD:
                pred_class = "Unknown"
                confidence = max_prob
            else:
                pred_class = classes[tf.argmax(pred[0]).numpy()]
                confidence = max_prob


            recommendations = get_comprehensive_recommendation(pred_class, confidence)


            try:
                if pred_class.lower() == "unknown":
                    pest_risk = get_pest_risk_assessment(api_key=app.config.get('WEATHER_API_KEY'), disease="Unknown")
                else:
                    pest_risk = get_pest_risk_assessment(api_key=app.config.get('WEATHER_API_KEY'))
            except Exception:
                pest_risk = None


            return render_template('index.html',
                                   prediction=pred_class,
                                   img_path=filename,
                                   confidence=confidence,
                                   recommendations=recommendations,
                                   pest_risk=pest_risk)
        
        except Exception as e:
            # Catch any unexpected exceptions and return error page
            error_msg = f"An error occurred: {str(e)}"
            return render_template('index.html',
                                   prediction=None,
                                   img_path=None,
                                   confidence=None,
                                   recommendations=None,
                                   pest_risk=None,
                                   error=error_msg), 500
    else:
        # GET request - just show landing page without prediction info
        try:
            pest_risk = get_pest_risk_assessment(api_key=app.config.get('WEATHER_API_KEY'))
        except Exception:
            pest_risk = None


        return render_template('index.html',
                               prediction=None,
                               img_path=None,
                               confidence=None,
                               recommendations=None,
                               pest_risk=pest_risk)



if __name__ == '__main__':
    app.run(debug=True)