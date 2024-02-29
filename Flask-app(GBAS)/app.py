from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'gbasnnos@gmail.com'  
app.config['MAIL_PASSWORD'] = 'gbasosnn2350'    

mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    selected_icons = db.Column(db.String(255))
    selected_category = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def page():
    return render_template('page.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('upmail')

    if not email:
        return 'Email is required for signup.', 400

    user_entry = User(email=email, selected_icons="", selected_category="")
    db.session.add(user_entry)
    db.session.commit()

    send_welcome_email(email)  # Send welcome email

    print('User signed up with the following email:')
    print(f'Email: {email}')

    return 'Signup successful!'

def send_welcome_email(email):
    msg = Message('Welcome to Icon App!', sender='your_email@gmail.com', recipients=[email])
    msg.body = 'Thank you for signing up! Here are your selected icons.'
    # Add logic to attach icons or provide necessary details in the email body

    mail.send(msg)

@app.route('/save_icons', methods=['POST'])
def save_icons():
    data = request.get_json()
    selected_icons = data.get('selectedIcons')
    selected_category = data.get('selectedCategory')
    user_email = data.get('userEmail')

    if not selected_icons or not selected_category or not user_email:
        return jsonify({'success': False, 'message': 'Invalid request parameters'}), 400

    user = User.query.filter_by(email=user_email).first()

    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    user.selected_icons = selected_icons
    user.selected_category = selected_category
    db.session.commit()

    return jsonify({'success': True, 'message': 'Icons saved successfully'})


@app.route('/userdata')
def get_user_data():
    users = User.query.all()
    user_data = [{'email': user.email, 'selectedIcons': user.selected_icons, 'selectedCategory': user.selected_category} for user in users]
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True)
