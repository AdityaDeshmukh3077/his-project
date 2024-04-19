from flask import Flask, render_template, request
app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET'])
@app.route('/login', methods=['POST'])
def home_page():
    if request.method == 'POST':
        print("Hello World!")
    else:
        return render_template('index.html')