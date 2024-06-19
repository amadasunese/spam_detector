from flask import Flask, request, jsonify, render_template, redirect
import joblib
import logging
import smtplib
import os

# Initialize Flask app and load the model
app = Flask(__name__)
model = joblib.load('spam_detector/spam_detector_model2.joblib')


# # Get the absolute path to the directory where the current script is located
# current_directory = os.path.spam_detector(os.path.abspath(__file__))

# # Construct the full path to the joblib file
# model_path = os.path.join(current_directory, 'spam_detector_model2.joblib')

# # Load the model
# model = joblib.load(model_path)


# model = joblib.load('spam_detector_model2.joblib')

# # Get the absolute path to the directory where the current script is located
# current_directory = os.path.dirname(os.path.abspath(__file__))

# # Construct the full path to the joblib file
# model_path = os.path.join(current_directory, 'spam_detector_model2.joblib')

# # Load the model
# model = joblib.load(model_path)


# Configure your email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'amadasunese@gmail.com'
EMAIL_HOST_PASSWORD = 'qxxo axga dzia jjsw'
RECIPIENT_ADDRESS = 'amadasunese@gmail.com'


# app.secret_key = "secret_key"


# # Configure Flask-Mail
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 465
# app.config["MAIL_USE_SSL"] = True
# app.config["MAIL_USERNAME"] = 'amadasunese@gmail.com'
# app.config["MAIL_PASSWORD"] = 'qxxo axga dzia jjsw'
# mail = Mail(app)


@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Email message setup
    email_message = f"Subject: Feedback from {name}\n\nFrom: {email}\n\nMessage: {message}"

    # Sending the email
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, RECIPIENT_ADDRESS, email_message)
        server.close()
        return 'Feedback sent successfully!'
    except Exception as e:
        return str(e)
        return redirect(url_for('home'))


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback_form.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact')

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
    app.run(debug=False)