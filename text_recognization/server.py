from flask import Flask, render_template
from flask import request, redirect, url_for
import textrec
app = Flask(__name__)

@app.route('/', methods = ["get"])
def index():
    return render_template('receipt.html')

@app.route("/", methods = ["post"])
def poster():
  data = request()
  print(data)
  return "hey"

@app.route('/results/')
def my_link():
    results = textrec.runner()
    return render_template('results.html', result=results)

@app.route('/receipt/run', methods = ['GET', 'POST'])
def run():
    if request.method == 'POST':
      names = []
      nums = request.form['number']
      for i in range(int(nums)):
        temp = 'p' + str(i + 1) + 'name' 
        names.append(request.form[temp])
    results = textrec.runner()
    return render_template('results.html', names=names, results=results)

@app.route('/getnames/')
def getNames():
   return 

    

if __name__ == '__main__':
  app.run(debug=True)