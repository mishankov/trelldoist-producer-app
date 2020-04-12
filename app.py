from flask import Flask

app = Flask(__name__)


@app.route('/api/webhooks/todoist/', methods=['GET', 'POST'])
def todoist_webhook():
    return 'ok'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
