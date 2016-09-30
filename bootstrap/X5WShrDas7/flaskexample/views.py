from flask import render_template, request, jsonify
from flaskexample import app



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#call from button on master
@app.route('/go')
def go():

    input_ = request.args.get('query', '')
    everythingOK=True
