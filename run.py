import os
from flask import redirect
from app import make_app

config_name = os.getenv('APP_SETTINGS')
app = make_app(config_name)
port = 5000


@app.route('/')
def rundoc():
    """method to run app documentation
    """
    return redirect('/apidocs/')


if __name__ == '__main__':
    app.run(port=port)
