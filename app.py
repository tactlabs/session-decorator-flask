'''

Source:
    

'''
from flask import Flask, render_template, request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def get_base():

    data = {
        'name' : 'Raja',
        'city' : 'Toronto'
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 3000)