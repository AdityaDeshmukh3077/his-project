from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/login')
def home_page():
    return render_template('index.html')