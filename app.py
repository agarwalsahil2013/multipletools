# Importing libraries
from flask import Flask, render_template, request, redirect, url_for, session, Response
from passwordchecker import read_file
import os
import PyPDF2
from PIL import Image

UPLOAD_FOLDER = 'uploadedfiles/'

# Flask configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Home page
@app.route("/", methods=["POST","GET"])
def home_page():
	return render_template('practice.html')

#all page route
@app.route('/<page_name>')
def blog(page_name):
	return render_template(page_name)

#jpg to png file upload
@app.route("/jpg2png.html", methods=["POST"])
def jpgtopngconverter():
	if request.method == "POST":
		uploaded_file = request.files["file1"]
		fname = uploaded_file.filename
		img = Image.open(uploaded_file)
		clean_name = os.path.splitext(fname)[0]
		img.save(f'static/{clean_name}.png','png')
		file_name = f"{clean_name}.png"
		return redirect(url_for('success', user = file_name))
	return render_template('jpg2png.html')

#showing and dowloading converted image
@app.route("/success/<user>")
def success(user):
	return render_template('jpg2png.html', unn = user, 
		message="Your file is ready to download")

#download png
@app.route("/downloadpng")
def downloadpng():
	name = os.listdir('static/')[0]
	file_path = f'static/{name}'
	img_open = Image.open(file_path)
	link = img_open.show()
	return Response(link, mimetype="image/png"), os.remove(file_path)

#pdfmerger file upload
@app.route("/upload", methods=["POST"])
def upload():
	merger = PyPDF2.PdfFileMerger()
	for uploaded_file in request.files.getlist("file[]"):
		if uploaded_file.filename != '':
			merger.append(uploaded_file)
	merger.write("uploadedfiles/CombinedAllPDF.pdf")
	return render_template('pdfmerger.html',message="Your file is ready to download here!!")

# combinedpdf link
@app.route("/combinedpdf")
def combinedpdf():
	with open('uploadedfiles/CombinedAllPDF.pdf', 'rb') as file:
		pdf = file.read()
	return Response(pdf, mimetype="application/pdf"), file.close(), os.remove('uploadedfiles/CombinedAllPDF.pdf')

#passwordchecker search bar
@app.route("/search", methods=["POST","GET"])
def search():
	if request.method == "POST":
		query = request.form['searchquery']
		count = read_file(password = str(query))
		return render_template('passwordcheck.html', count=count)
	else:
		return render_template('passwordcheck.html')

#passwordchecker file upload
@app.route("/file_upload", methods=["POST","GET"])
def file_upload():
	if request.method == "POST":
		uploaded_file = request.files["file"]
		if uploaded_file.filename.split(".")[-1] == "txt":	
			path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
			uploaded_file.save(path)

			counts = read_file(file_loc=path)
			return render_template('passwordcheck.html', counts = counts), os.remove(path)
		else:
			return render_template('passwordcheck.html', message="Please upload .txt file") 
	else:
		return render_template("passwordcheck.html")

