import os
from flask import (
    Flask,
    request,
    render_template
)
from requests import request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def status():
    return render_template(
        'build-monitor.html',
        preview_admin=is_up("https://www.notify.works/_status"),
        preview_api=is_up("https://api.notify.works/status/_status"),
        staging_admin=is_up("https://staging.notifications.service.gov.uk/_status"),
        staging_api=is_up("https://staging-api.notifications.service.gov.uk/status/_status")
    )


def is_up(url):
    response = request(
        "GET",
        url
    ).status_code
    return response == 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6001))
    app.run(host='0.0.0.0', port=port)
