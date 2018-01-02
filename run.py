import os
from flask import redirect
from app import make_app
config_name = os.getenv('APP_SETTINGS') # config_name = "development"

app = make_app(config_name)
port = int(os.environ.get('PORT', 5000))
host = "127.0.0.1"

@app.route('/')
def Rundocs():
    """method to run app documentation
    """
    return redirect('/apidocs/')

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
