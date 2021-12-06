import datetime
from flask import Flask, render_template, request
import logging



#------------------Defines flask app as "__name__"------------------
app = Flask(__name__)

#------------------DEFINE APP ROUTES----------
@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/userOrders')
def userOrders():
    return render_template('userOrders.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
def register():
    return render_template('account.html')   


@app.route('/submitted_order', methods=['POST'])
def submitted_order():
    name = request.form['name']
    email = request.form['email']
    item = request.form['item']
    address = request.form['address']
    postcode = request.form['postcode']
    eta = request.form['eta']
   
    return render_template(
    'submitted_order.html',
        name=name,
        email=email,
        item=item,
        address=address,
        postcode=postcode,
        eta=eta)



#------------------Error Handlers----------
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#------------------If we run this in python directly----------
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
