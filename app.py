# Importing libraries
from flask import Flask, render_template, request, redirect, url_for, session, Response
from passwordchecker import read_file
import os
import PyPDF2
from PIL import Image

UPLOAD_FOLDER = 'static/'

# Flask configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Home page
@app.route("/")
@app.route("/home")
def home():
	return render_template('practice.html', title="Home")

#jpg to png file upload
@app.route("/jpg2png", methods=["GET","POST"])
def jpgtopngconverter():
	if request.method == "POST":
		uploaded_file = request.files["file1"]
		if uploaded_file.filename.split(".")[-1] in ["jpg","JPG"]:	
			fname = uploaded_file.filename
			img = Image.open(uploaded_file)
			clean_name = os.path.splitext(fname)[0]
			img.save(f'static/{clean_name}.png','png')
			file_name = f"{clean_name}.png"
			file_path = f"static/{clean_name}.png"
			return render_template('jpg2png.html', unn = file_name, 
							message="Your file is ready to download")
		return render_template('jpg2png.html', message="File not in JPG format!!")
	return render_template('jpg2png.html', title='JPG2PNG')

#pdfmerger file upload
@app.route("/pdfmerger", methods=["GET","POST"])
def pdfmerger():
	if request.method == "POST":
		merger = PyPDF2.PdfFileMerger()
		for uploaded_file in request.files.getlist("file[]"):
			if uploaded_file.filename != '':
				merger.append(uploaded_file)
		merger.write("static/CombinedAllPDF.pdf")

		return render_template('pdfmerger.html',
							message="Your file is ready to download here!!")
	return render_template('pdfmerger.html', title='PDFMerger')

# combinedpdf link
@app.route("/combinedpdf")
def combinedpdf():
	with open('static/CombinedAllPDF.pdf', 'rb') as file:
		pdf = file.read()
	return Response(pdf, mimetype="application/pdf"), file.close(), os.remove('static/CombinedAllPDF.pdf')

#passwordchecker search bar
@app.route("/passwordcheck", methods=["POST","GET"])
def passwordcheck():
	if request.method == "POST":
		query = request.form['searchquery']
		count = read_file(password = str(query))
		return render_template('passwordcheck.html', count=count)	
	return render_template('passwordcheck.html', title='PassCheck')

#passwordchecker file upload
@app.route("/file_upload", methods=["POST","GET"])
def file_upload():
	if request.method == "POST":
		uploaded_file = request.files["file"]
		if uploaded_file.filename.split(".")[-1] == "txt":	
			path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
			uploaded_file.save(path)

			counts = read_file(file_loc=path)
			return render_template('passwordcheck.html', counts=counts), os.remove(path)
		return render_template('passwordcheck.html', message="Please upload .txt file") 
	else:
		return render_template("passwordcheck.html")


if __name__ == '__main__':
    app.run(debug=True)

