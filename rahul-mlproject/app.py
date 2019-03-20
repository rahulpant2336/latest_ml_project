from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import hashlib
import datetime
import json
import pickle
import numpy as np
import requests

app = Flask(__name__)

app.secret_key = '3242353645646'





@app.route('/')
def login():
    return render_template('login.html')


@app.route('/request',methods=['POST'])
def hello_world():
   import requests
   rahul = request.form['Name']
   rahul1 = json.loads(rahul)

   check_result = model.predict([[rahul1]])

   flash("Salary must be around "+str(int(check_result)))

   return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('modle.html', now=datetime.datetime.now())
    else:
        return redirect(url_for('login'))




@app.route('/login-check', methods = ['POST'])
def checkLogin():
    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])
        if request.method == 'POST':
            if request.form['email'] != 'rahul.pant@adaan.com' or request.form['password'] != 'rahul2336':
                flash("Invalid Credentials")
                return redirect(url_for('login'))
            else:
                data = ('Rahul',request.form['email'],request.form['password'],1)
                session['username'] = data
                return redirect(url_for('dashboard'))




@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


#KNN IRIS
# Loading model to compare the results
iris_model = pickle.load(open('knn_iris_model.pkl','rb'))
@app.route('/knn_iris')
def knnIris():
    if 'username' in session:
        username = session['username']
        return render_template('knn_iris.html', now=datetime.datetime.now())
    else:
        return redirect(url_for('login'))


@app.route('/request_iris',methods=['POST'])
def modelIris():
   import requests
   sepal_length = request.form['sepal_length']
   sepal_width = request.form['sepal_width']
   petal_length = request.form['petal_length']
   petal_width = request.form['petal_width']
   sepal_length_json = json.loads(sepal_length)
   sepal_width_json = json.loads(sepal_width)
   petal_length_json = json.loads(petal_length)
   petal_width_json = json.loads(petal_width)

   check_result = iris_model.predict(np.asarray([[sepal_length_json,sepal_width_json,petal_length_json,petal_width_json]]))

   flash("Category of iris flower is "+str(check_result[0]))

   return redirect(url_for('knnIris'))




if __name__ == "__main__":
    app.run(debug=True)
