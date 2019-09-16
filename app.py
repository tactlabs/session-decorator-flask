'''

Source:
    

'''
from flask import Flask, render_template, request
from flask import jsonify, session
from functools import wraps

app = Flask(__name__)

# Constatns
SAMPLE_USERID = 1001
SAMPLE_USERNAME = "raja"
SAMPLE_PASSWORD = "raja"
SESSION_PRE     = "se_"
SESSION_POST    = "_ssyd"
EMPTY           = ""

@app.route('/')
def get_base():

    data = {
        'name' : 'Base',
        'city' : 'Unknown'
    }

    return jsonify(data)

def requires_auth(f):
  
    @wraps(f)
    def decorated(*args, **kwargs):
    
        # check apikey in args
        sid = request.values.get("sid")

        if(not sid):

            data = {
                'apiresult' : 104,
                'apimessage': 'Login Required'
            }

            return jsonify(data)

        print('sid : '+str(sid))

        if(validate_sessionid(sid)):

            data = {
                'apiresult' : 105,
                'apimessage': 'Session Required'
            }

            return jsonify(data)

        return f(*args, **kwargs)

    return decorated

@app.route('/user')
@requires_auth
def get_user():

    data = {
        'name' : 'Raja',
        'city' : 'Toronto'
    }

    return jsonify(data)

def validate_user(username, password):

    if(username == SAMPLE_USERNAME and password == SAMPLE_PASSWORD):
        return SESSION_PRE+str(SAMPLE_USERID) + SESSION_POST

    return None

def validate_sessionid(sid):

    if(sid is None):
        return False

    sid = sid.replace(SESSION_PRE, EMPTY)
    userid = sid.replace(SESSION_POST, EMPTY)

    userid = int(userid)

    if(userid == SAMPLE_USERID):
        return False

    return True

@app.route('/login')
def login():

    username = request.values.get("username")
    password = request.values.get("password")

    sid = validate_user(username, password)

    if(sid):

        # Store the user information in flask session.
        #session['sid'] = sid

        data = {
            'userid' : sid,
            'name' : 'Raja',
            'city' : 'Toronto',
            'sid' : sid
        }

        return jsonify(data)

    data = {
        'apiresult' : 103,
        'apimessage': 'Login Failed'
    }

    return jsonify(data)



@app.route('/logout')
def logout():

    # Clear session stored data
    #session.clear()

    data = {
        'apierror' : 0,
        'apimessage' : 'None'
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 3000)