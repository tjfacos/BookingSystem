import os
from flask import *

from blueprints.auth import auth
from blueprints.home import home

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev',
    )

def RegisterBlueprints(blueprints: list[Blueprint]):
    for bp in blueprints:
        app.register_blueprint(bp)



RegisterBlueprints([
    auth.bp,
    home.bp
])

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