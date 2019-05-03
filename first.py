from flask import Flask, render_template, request
from werkzeug import secure_filename
import requests

api_key = 'acc_2a102c139578fc5'
api_secret = 'c8f40fa8abc5899255890268cac10182'



app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():

	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		image_path=f.filename
		response = requests.post('https://api.imagga.com/v2/tags',auth=(api_key, api_secret),files={'image': open(image_path, 'rb')})
		answer=response.json()
		q1=answer["result"]
		q2=q1["tags"]
		q3=[]
		count=0
		for i in q2:
			if(count>4):
				break
			count+=1
			q4=i["tag"]
			q5=q4["en"]
			q3.append(q5)
		query=q3
	return render_template('second.html',query=query)
        
if __name__ == '__main__':
   app.run(debug = True)