import os
from flask import *

# from db import *

from auth import auth

app = Flask(__name__)

app.register_blueprint(
    auth.bp
)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(
            app.root_path, 
            'assets'
        ),
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )


def main():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()