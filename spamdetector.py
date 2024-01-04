from flask import Flask, request, jsonify, render_template
import joblib
import logging

# Initialize Flask app and load the model
app = Flask(__name__)
model = joblib.load('spam_detector_model.joblib')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Input validation
        email_text = request.form.get('text', '')
        if not email_text:
            app.logger.warning('No email text provided')
            return jsonify({'error': 'No email text provided'}), 400

        # Model prediction
        prediction = model.predict([email_text])
        app.logger.info('Prediction made for an email')
        return jsonify({'spam': bool(prediction[0])})

    except Exception as e:
        # Error handling
        app.logger.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': 'Error occurred during prediction'}), 500

@app.errorhandler(404)
def page_not_found(e):
    # Custom error handler for 404 Not Found
    app.logger.warning('Page not found')
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    # Custom error handler for 500 Internal Server Error
    app.logger.error('Internal server error')
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
