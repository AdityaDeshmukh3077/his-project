from flask import Flask, render_template, request
import util


app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET'])
@app.route('/login', methods=['POST'])
def home_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if util.check_username_password(username, password):
            return render_template('forms1.html')
        else:
            message = "Invalid username or password"
            return render_template('index.html', message=message)
    else:
        return render_template('index.html')
    
@app.route('/analysis', methods=['POST'])
def patient_details():
    return render_template('index.html')