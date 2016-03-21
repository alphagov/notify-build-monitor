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

    return render_template(
        'build-monitor.html',
        preview_admin=preview_admin,
        preview_api=preview_api,
        staging_admin=staging_admin,
        staging_api=staging_api,
        master_api_build=master('https://api.travis-ci.org/repos/alphagov/notifications-api/branches/master'),
        master_admin_build=master('https://api.travis-ci.org/repos/alphagov/notifications-admin/branches/master'),
        staging_api_build=master('https://api.travis-ci.org/repos/alphagov/notifications-api/branches/staging'),
        staging_admin_build=master('https://api.travis-ci.org/repos/alphagov/notifications-admin/branches/staging')
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
    status = response.json()['branch']['state']
    if status == "":
        return None
    if status == "passed":
        return True
    return False


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6001))
    app.run(host='0.0.0.0', port=port)
