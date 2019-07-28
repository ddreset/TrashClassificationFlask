import os
import label_image as label
from flask import Flask, request, json, render_template, redirect, url_for
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import base64
import requests

# UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])

app = Flask(__name__)
api = Api(app)
app.debug = True
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

image_type = ""
image_string = ""
garbage_text = ""

class Classification(Resource):
    def post(self):
        # get image
        try:
            # if the post request does NOT have the file part
            # try to get imageURL
            if 'image' not in request.files:
                request_data = request.get_json()
                imageURL = request_data['imageURL']
                print("imageURL: "+imageURL)
                # check image format
                if not allowed_file(imageURL):
                    return {'errorMessage': 'Does not support this file format...'}, 500
                print("format check pass!")
                if(len(imageURL)<=0):
                    return {'errorMessage': 'No image found in this request...'}, 500
                else:
                    print("getting image content from url...")
                    image_string = base64.b64encode(requests.get(imageURL).content).decode('utf-8')
            else:
                # if post request has file part
                # get image from it
                image = request.files['image']
                if image.filename == '':
                    return {'errorMessage': 'Please, provide a fileName...'}, 500
                # check image format
                if not allowed_file(image.filename):
                    return {'errorMessage': 'Does not support this file format...'}, 500

                print("format check pass!")
                # encode image by base64
                image_string = base64.b64encode(image.read()).decode('utf-8')

            print("got image!")

            # if there is another save or read
            # should move pointer to the beginning of file
            # image.seek(0)

            # save image to local
            # filename = secure_filename(image.filename)
            # image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # imageURL = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # imageURL = request.base_url.split('/classify')[0]+'/'+os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
        except:
            return {'errorMessage': 'Wrong request'}, 500
    
        # classfify image
        parameters = ["--graph","garbage_output.pb","--labels","garbage_labels.txt","--input_layer","Placeholder","--output_layer","final_result","--image",image_string]
        results = label.main(parameters)
        data = {results[0,0]:results[0,1],results[1,0]:results[1,1],results[2,0]:results[2,1],results[3,0]:results[3,1],results[4,0]:results[4,1],results[5,0]:results[5,1]}
        if app.debug:
            print(data)
        response, err = data,"error"
            
        # delete image
        # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # return results
        if response:
            garbage_text = data
            return {'result':data, 'image': "data:image/"+image_type+";base64,"+image_string}, 200
        else:
            garbage_text = error
            return {'errorMessage': err}, 404

def allowed_file(filename):
    if '.' in filename:
        image_type = filename.rsplit('.', 1)[1].lower()
        return image_type in ALLOWED_EXTENSIONS
    return False

api.add_resource(Classification, '/classify')

@app.route('/')
def index():
    return render_template('webapp.html')

@app.route('/show/<image_name>')
def show_image(image_name):
    full_filename = '../'+os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    return render_template("showImage.html", request_image = full_filename)

if __name__ == "__main__":
    app.run()