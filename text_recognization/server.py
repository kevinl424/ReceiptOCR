from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import textrec
import os

app = Flask(__name__)

# make instance folder for users to upload receipt documents
os.makedirs(os.path.join(app.instance_path, 'imgdir'), exist_ok=True)
app.config.update(SECRET_KEY='supermarket', ENV='development')


@app.route('/', methods=["get"])
def index():
    return render_template('receipt.html')


@app.route("/", methods=["post"])
def poster():
    data = request()
    print(data)
    return "hey"


@app.route('/results/')
def results():
    return render_template('results.html', result=session['results'], names=session['names'])


@app.route('/receipt/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        names = []
        nums = request.form['number']
        for i in range(int(nums)):
            # get the names of the people splitting the bill
            temp = 'p' + str(i + 1) + 'name'
            names.append(request.form[temp])
        session['names'] = names

        # call for the file uploaded
        f = request.files['image']
        # define the path in the instance folder
        filepath = os.path.join(app.instance_path, 'imgdir', secure_filename(f.filename))
        f.save(filepath)
        session['results'] = textrec.runner(filepath)  # passing in filepath for image to be read
        #????
        session.permanent = True
    # results = textrec.runner()
    return redirect(url_for('results'))


@app.route('/costs/')
def costs():
    return


if __name__ == '__main__':

    app.run(debug=True)
