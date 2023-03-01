from flask import Flask, render_template
from flask import request
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
    

if __name__ == '__main__':
  app.run(debug=True)