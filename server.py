from flask import Flask, url_for

my_app = Flask(__name__)


@my_app.route('/hello/')
def hello():
    return "Hello.  How are you today?"


@my_app.route('/goodbye/')
@my_app.route('/goodbye/<your_name>/')
def goodbye(your_name="Anonymous User"):
    return "Goodbye {}".format(your_name)


def create_url_html(method_name, link_text=None):
    if link_text==None:
        link_text=method_name

    url = url_for(method_name)
    return "<li><a href='{}'>{}</a></li>".format(url, link_text)


@my_app.route('/')
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


@my_app.route('/GroupOne/')
def group_one():
    return "Welcome group one, develop here"


@my_app.route('/GroupTwo/')
def group_two():
    return "Welcome group two, develop here"


@my_app.route('/GroupThree/')
def group_three():
    return "Welcome group three, develop here"


@my_app.route('/GroupFour/')
def group_four():
    return "Welcome group four, develop here"


@my_app.route('/GroupFive/')
def group_five():
    return "Welcome group five, develop here"


if __name__ == "__main__":
    """Start the server
    host  -- (default '127.0.0.1')
    port  -- (default 5000)
    debug -- set to True to reload every time a change is detected: very useful! (default False)

    """
    my_app.run(host='localhost', port=5678, debug=True)
