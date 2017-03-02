import os
from flask import (
    Flask,
    render_template,
    jsonify,
    make_response
)
from flask import request as flask_req
from requests import request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def status():
    preview_admin = is_up("https://www.notify.works/_status")
    preview_api = is_up("https://api.notify.works/_status")

    return render_template(
        'build-monitor.html',
        preview_admin=preview_admin,
        preview_api=preview_api
    )


@app.route('/deploys/<repo>/<base>...<target>.svg', methods=['GET'])
def deploys(repo, base, target):

    prefix = flask_req.args.get('prefix', '')

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
    ]) - 1  # we shouldn’t count the final merge from parent branch

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


@app.route('/notifications/sms/mmg', methods=['POST'])
def temp_mmg_delivery_receipt():
    print('Posted delivery receipt from mmg: {}'.format(flask_req.form))
    print('Posted delivery receipt from mmg: {}'.format(flask_req.data))
    print('Posted delivery receipt from mmg ID: {}, MSISDN: {}, Delivery: {}, CID: {}'
          .format(flask_req.args.get('ID', None),
                  flask_req.args.get('MSISDN', None),
                  flask_req.args.get('Delivery', None),
                  flask_req.args.get('CID', None)))

    return jsonify(result='success'), 200

@app.route('/notifications/sms/mmg/response', methods=['POST'])
def temp_mmg_delivery_receipt():
    print('Posted delivery receipt from mmg: {}'.format(flask_req.form))
    print('Posted delivery receipt from mmg: {}'.format(flask_req.data))
    return jsonify(result='success'), 200


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
    app.run(host='0.0.0.0', port=port, debug=True)
