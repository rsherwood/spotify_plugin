from flask import Flask, url_for
from RS.rs import page_rs

my_app = Flask(__name__)


@my_app.route('/greet/<your_name>/')
def personalised_hello(your_name):
    return "Hello {}.  How are you today?".format(your_name)


@my_app.route('/goodbye/')
def bye():
    return "Seeya!"


@my_app.route('/pretty/<your_name>/')
def templated_hello(your_name):
    username = your_name
    custom_string = "Hello! What a pleasure it is to see you!"
    return "xyz"


@my_app.route('/')
def hello():
    print url_for('personalised_hello', your_name='Russell')
    print url_for('bye', your_name='Russell')
    print url_for('templated_hello', your_name='Russell')
    return "xyz"


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
