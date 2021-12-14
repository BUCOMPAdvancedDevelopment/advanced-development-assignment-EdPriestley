#import packages needed
import datetime
from flask import Flask, render_template, request, jsonify,redirect, url_for
import json
import requests
from google.auth.transport import requests as grequests
from google.cloud import datastore
import google.oauth2.id_token
import pymongo
import logging
from bson.objectid import ObjectId

#connect to firebase
firebase_request_adapter = grequests.Request()

# [START gae_python38_datastore_store_and_fetch_user_times]
# [START gae_python3_datastore_store_and_fetch_user_times]
datastore_client = datastore.Client()

#configure flask
app = Flask(__name__)


#Get users email from firebase
def store_time(email, dt):
    entity = datastore.Entity(key=datastore_client.key('User', email, 'visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


#Get the last 3 logind of user from firebase
def fetch_times(email, limit):
    ancestor = datastore_client.key('User', email)
    query = datastore_client.query(kind='visit', ancestor=ancestor)
    query.order = ['-timestamp']
    times = query.fetch(limit=limit)
    return times


#Configure MongoDB connection
mongoClient = pymongo.MongoClient(
   "mongodb+srv://edward:Edward99@assignment.8snc4.mongodb.net/assignment?retryWrites=true&w=majority")
mongoDB = mongoClient['ADUnit']


# Stores the order into Mongo collection
def store_post_mongodb(name, email, item, address, postcode, eta):
    collection = mongoDB['orders']
    # email will not be added, as author parameter will be used to identify individual users posts
    json_data = {"name": name, "email": email, "item": item, "address": address,
                 "postcode": postcode,"eta": eta}
    collection.insert_one(json_data).inserted_id    

# Amends the order into Mongo collection 
def amend_post_mongodb(orderNo, name, email, item, postcode, address, eta):
    collection = mongoDB['orders']
    query = {"_id": ObjectId(orderNo)}
    newData = {"name": name, "email": email, "item": item, "address": address,
                 "postcode": postcode,"eta": eta}
    collection.replace_one(query, newData)


# delete the order into Mongo collection 
def delete_post_mongodb(orderNo):
    collection = mongoDB['orders']
    query = {"_id": ObjectId(orderNo)}
    collection.delete_one(query)


#------------------Define Routes----------
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')


@app.route('/account')
def account():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            store_time(claims['email'], datetime.datetime.now())
            times = fetch_times(claims['email'], 3)
           

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
    else:
        return redirect("/login")

    return render_template(
        'account.html',
        user_data=claims, error_message=error_message, times=times)


@app.route('/userOrders')
def getOrders():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            email=claims['email']
            url = "https://europe-west2-assignment-332511.cloudfunctions.net/helloworld?email=" + email
            uResponse = requests.get(url)
            jResponse = uResponse.text
            data = json.loads(jResponse)
        
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
    else:
        return redirect("/login")
    return render_template('userOrders.html', data=data) 



@app.route('/newOrder')
def newOrder():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
    else:
        return redirect("/login")
    return render_template(
        'newOrder.html')

    


@app.route('/subOrder',methods=['GET', 'POST'])
def subOrder():
    return render_template('afterOrder.html', name=name, email=email, item=item, address=address, postcode=postcode, eta=eta)


#------------------Amend Orders----------
@app.route('/amendOrder')
def amendOrder():
    return render_template(
        'amendOrder.html') 


@app.route('/afterAmend', methods=['GET', 'POST'])
def afterAmend():
    if request.method=='GET':
        return render_template('home.html')   
    else:
        orderNo = request.form['orderNo']
        name = request.form['name']
        email = request.form['email']
        item = request.form['item']
        address = request.form['address']
        postcode = request.form['postcode']
        eta = datetime.datetime.now() + datetime.timedelta(days=7)
        eta = eta.date().strftime("%d%m%Y")
        amend_post_mongodb(orderNo, name, email, item, address, postcode, eta)
        return render_template('afterAmend.html', orderNo=orderNo, name=name, email=email, item=item, address=address, postcode=postcode, eta=eta)




#------------------Delete Orders----------
@app.route('/deleteOrder')
def deleteOrder():
    return render_template(
        'deleteOrder.html')


@app.route('/afterDelete', methods=['GET', 'POST'])
def afterDelete():
    if request.method=='GET':
        return render_template('home.html')   
    else:
        orderNo = request.form['orderNo']
        delete_post_mongodb(orderNo)
        return render_template('afterDelete.html', orderNo=orderNo)


 

#------------------Error Handlers----------
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404




if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
