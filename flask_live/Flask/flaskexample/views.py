from flask import render_template, request, jsonify
from flaskexample import app
#from pyzipcode import ZipCodeDatabase
import Model_Run_22sep
import Model_Run_29sep0
#import Model_Run_15sep
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database
# import pandas as pd
# import psycopg2


@app.route('/')
@app.route('/index')
def index():
    return render_template('master.html')

@app.route('/go')
def go():
    #zcdb=ZipCodeDatabase()
    input_ = request.args.get('query', '')
    everythingOK=True
    # try:
    #     everythingOK=True
    #     zips=zcdb.find_zip(state=stateinput)
    #     zips=[int(z.zip) for z in zips]
    # except:
    #     everythingOK=False

    if everythingOK:
        predict=Model_Run_29sep0.main(input_)
    else:
        predict='Input not understood'
    # new= [render_template('go.html',query = item) for item in predicttown]
    return render_template(
        'go.html',
        query = predict
    )


# go([92037,93430,92014,92030])
