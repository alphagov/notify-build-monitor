import os
import json
from flask import (
    Flask,
    render_template,
    make_response
)
from flask import request as flask_request
from requests import request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def status():

    return render_template(
        'build-monitor.html',
        preview_admin=is_up("https://www.notify.works/_status"),
        preview_api=is_up("https://api.notify.works/_status"),
        staging_admin=is_up("https://staging.notifications.service.gov.uk/_status"),
        staging_api=is_up("https://staging-api.notifications.service.gov.uk/_status"),
        live_admin=is_up("https://www.notifications.service.gov.uk/_status"),
        live_api=is_up("https://api.notifications.service.gov.uk/_status"),
        master_api_build=master('https://api.travis-ci.org/repos/alphagov/notifications-api/branches/master'),
        master_admin_build=master('https://api.travis-ci.org/repos/alphagov/notifications-admin/branches/master'),
        staging_api_build=master('https://api.travis-ci.org/repos/alphagov/notifications-api/branches/staging'),
        staging_admin_build=master('https://api.travis-ci.org/repos/alphagov/notifications-admin/branches/staging'),
        live_api_build=master('https://api.travis-ci.org/repos/alphagov/notifications-api/branches/live'),
        live_admin_build=master('https://api.travis-ci.org/repos/alphagov/notifications-admin/branches/live')
    )


@app.route('/deploys/<repo>/<base>...<target>.svg', methods=['GET'])
def deploys(repo, base, target):

    prefix = flask_request.args.get('prefix', '')

    response = request(
        "GET",
        'https://api.github.com/repos/alphagov/{}/compare/{}...{}'.format(repo, base, target),
        headers={
            'Authorization': 'token {}'.format(os.environ['GITHUB_API_KEY'])
        }
    )

    response = response.json()
    commits_ahead = response.get('ahead_by')

    merges_ahead = len([
        commit for commit in response.get('commits') if len(commit.get('parents')) > 1
    ])

    svg = render_template(
        'deploy.svg',
        merges_ahead=merges_ahead,
        target=target,
        base=base,
        prefix=prefix,
        background='#B10E1E' if merges_ahead > 1 else '#F47738' if merges_ahead == 1 else '#335b00'
    )

    svg_response = make_response(svg)
    svg_response.headers["Content-Type"] = "image/svg+xml"

    return svg_response


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
