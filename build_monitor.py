import os
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def status():
    return "status"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6001))	
    app.run(host='0.0.0.0', port=port)
