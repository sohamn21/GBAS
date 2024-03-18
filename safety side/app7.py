from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Function to fetch icons associated with the provided Gmail address
def fetch_icons(gmail):
    try:
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        cursor.execute("SELECT icon1, icon2 FROM UserData WHERE gmail = ?", (gmail,))
        icons = cursor.fetchone()
        conn.close()
        return icons  # Return the icons in the correct order
    except Exception as e:
        print("Error fetching icons:", e)
        return None

# Function to authenticate the selected icons
# Function to authenticate the selected icons
# Function to authenticate the selected icons
def authenticate(icon1, icon2, gmail):
    try:
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        cursor.execute("SELECT icon1, icon2 FROM UserData WHERE gmail = ?", (gmail,))
        user_icons = cursor.fetchone()
        conn.close()

        print("Received Icon 1:", icon1)
        print("Received Icon 2:", icon2)
        print("Received Gmail:", gmail)
        print("Icons from database:", user_icons)

        if user_icons and set(user_icons) == set([icon1, icon2]):
            return True
        else:
            return False
    except Exception as e:
        print("Error authenticating icons:", e)
        return False




 

# Function to generate a shuffled list of icons
def generate_shuffled_icons():
    try:
        icon_paths = []
        for category in ['Alphabets', 'Flag', 'Numbers', 'Transportation']:
            for i in range(1, 17):
                icon_paths.append(f'static/images/{category}/{category}{i}.png')
        random.shuffle(icon_paths)
        return icon_paths
    except Exception as e:
        print("Error generating shuffled icons:", e)
        return None

@app.route('/')
def signin_page():
    return render_template('signin.html')

# Route to handle the "Next" button click
@app.route('/next', methods=['POST'])
def next_step():
    try:
        gmail = request.form['gmail']
        print("Received Gmail:", gmail)
        icons = fetch_icons(gmail)
        print("Received icons:", icons)
        if icons:
            shuffled_icons = generate_shuffled_icons()
            return jsonify({'status': 'success', 'shuffled_icons': shuffled_icons})
        else:
            return jsonify({'status': 'error', 'message': 'User not found'})
    except Exception as e:
        print("Error processing next step:", e)
        return jsonify({'status': 'error', 'message': 'An error occurred'})

# Route to handle the signin form submission
@app.route('/signin', methods=['POST'])
def signin():
    try:
        icon1 = request.form['icon1']
        icon2 = request.form['icon2']
        gmail = request.form['gmail']

        print("Received Icon 1:", icon1)
        print("Received Icon 2:", icon2)
        print("Received Gmail:", gmail)

        if authenticate(icon1, icon2, gmail):
            return jsonify({'status': 'success', 'message': 'Authentication successful!'})
        else:
            return jsonify({'status': 'error', 'message': 'Authentication failed. Please try again.'})
    except Exception as e:
        print("Error processing signin request:", e)
        return jsonify({'status': 'error', 'message': 'An error occurred during authentication.'})


if __name__ == '__main__':
    app.run(debug=True)
