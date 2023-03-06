from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import textrec
import os

app = Flask(__name__)

#make instance folder for users to upload receipt documents
os.makedirs(os.path.join(app.instance_path, 'imgdir'), exist_ok=True)

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
        #get the names of the people splitting the bill
        temp = 'p' + str(i + 1) + 'name' 
        names.append(request.form[temp])
      
      #call for the file uploaded
      f = request.files['image']
      #define the path in the instance folder
      filepath = os.path.join(app.instance_path, 'imgdir', secure_filename(f.filename))
      f.save(filepath)
      results = textrec.runner(filepath) #passing in filepath for image to be read

    # results = textrec.runner()
    return render_template('results.html', names=names, results=results)

@app.route('/getnames/')
def getNames():
   return 

    

if __name__ == '__main__':
  app.run(debug=True)