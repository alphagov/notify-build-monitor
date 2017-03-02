import os
from flask import (
    Flask,
    render_template
)
from requests import request

app = Flask(__name__)


@app.route('/lag')
def deploy_lag():
    return render_template('deploy-lag-radiator.html')


@app.route('/', methods=['GET'])
def status():
    preview_admin = is_up("https://www.notify.works/_status")
    preview_api = is_up("https://api.notify.works/_status")

    return render_template(
        'build-monitor.html',
        preview_admin=preview_admin,
        preview_api=preview_api
    )


def is_up(url):
    response = request(
        "GET",
        url
    ).status_code
    return response == 200


def master(url):
    response = request(
        "GET",
        url,
        headers={'Accept': 'application/vnd.travis-ci.2+json'}
    )
    return response.json()['branch']['state'] in ["", 'passed']


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6001))
    app.run(host='0.0.0.0', port=port)
