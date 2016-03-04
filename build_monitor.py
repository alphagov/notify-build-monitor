import os
from flask import (
    Flask,
    render_template
)
from requests import request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def status():
    preview_admin = is_up("https://www.notify.works/_status")
    preview_api = is_up("https://api.notify.works/_status")
    staging_admin = is_up("https://staging.notifications.service.gov.uk/_status")
    staging_api = is_up("https://staging-api.notifications.service.gov.uk/_status")
    has_failing_build = False

    if not preview_admin or not preview_api or not staging_admin or not staging_api:
        has_failing_build = True

    return render_template(
        'build-monitor.html',
        has_failing_build=has_failing_build,
        preview_admin=preview_admin,
        preview_api=preview_api,
        staging_admin=staging_admin,
        staging_api=staging_api
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
