from flask import Flask, url_for, send_from_directory
import os

app = Flask(__name__)


@app.route('/hello/')
def hello():
    return "Hello.  How are you today?"


@app.route('/goodbye/')
@app.route('/goodbye/<your_name>/')
def goodbye(your_name="Anonymous User"):
    return "Goodbye {}".format(your_name)


def create_url_html(method_name, link_text=None):
    if link_text==None:
        link_text=method_name

    url = url_for(method_name)
    return "<li><a href='{}'>{}</a></li>".format(url, link_text)


@app.route('/')
def index():
    urls = "<ul>"
    urls += create_url_html('hello')
    urls += create_url_html('goodbye')
    urls += create_url_html('group_one')
    urls += create_url_html('group_two')
    urls += create_url_html('group_three')
    urls += create_url_html('group_four')
    urls += create_url_html('group_five')
    urls += "</ul>"
    return urls


@app.route('/GroupOne/')
def group_one():
    return "Welcome group one, develop here."


@app.route('/GroupTwo/')
def group_two():
    return "Welcome group two, develop here"


@app.route('/GroupThree/')
def group_three():
    return "Welcome group three, develop here"


@app.route('/GroupFour/')
def group_four():
    return "Welcome group four, develop here"


@app.route('/GroupFive/')
def group_five():
    return "Welcome group five, develop here"


if __name__ == "__main__":
    """Start the server
    host  -- (default '127.0.0.1')
    port  -- (default 5000)
    debug -- set to True to reload every time a change is detected: very useful! (default False)

    """
    app.run(host='localhost', port=5000, debug=True)
    app.add_url_rule('/favicon.ico/', redirect_to=url_for('static', filename='favicon.ico'))
