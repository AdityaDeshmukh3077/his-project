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
            print("Hello World")
    else:
        return render_template('index.html')