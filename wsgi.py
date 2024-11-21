from flask import Flask
from settings import Config
from app.route import api_v1, default

app = Flask(__name__)

app.config.from_object(Config)

# Register Blueprint
app.register_blueprint(default)  # default routes Blueprint
app.register_blueprint(api_v1)   # api_v1 routes Blueprint


@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['expires'] = 0
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888)
