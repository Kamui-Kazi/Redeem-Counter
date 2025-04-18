from app import app
from flask import render_template, request
from write_file import write
from bots import start


@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/bots', methods=['GET'])
def run_bots():
    start()
    return "bots are running"

@app.route('/form', methods=['GET'])
def blank_form():
    return render_template('form.html')

@app.route('/form/submited', methods=['POST'])
def submited():
    data_dict = {
        'client_id' : request.form['client_id'],
        'client_secret' : request.form['client_secret'],
        'bot_name' : request.form['bot_name'],
        'bot_id' : request.form['bot_id'],
        'owner_name' : request.form['owner_name'],
        'owner_id' : request.form['owner_id'],
        'target_name' : request.form['target_name'],
        'target_id' : request.form['target_id'],
    }
    
    #if the target is left blank then default to the owner
    if data_dict['target_name'] == "" or data_dict['target_id'] == "":
        data_dict['target_name'] = data_dict['owner_name']
        data_dict['target_id'] = data_dict['owner_id']
        
    write(data_dict)
    return render_template('submited.html', data_dict = data_dict)