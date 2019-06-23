import label_image as label
from flask import Flask, request, json, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
app.debug = True

imageURL = ""
garbage_text = ""

class Classification(Resource):
    def post(self):
        try:
            request_data = request.get_json()
            print(request_data)
            imageURL = request_data['imageURL']
        except:
            return {'errorMessage': 'Wrong request...'}, 500
        if(len(imageURL)>0):
            parameters = ["--graph","garbage_output.pb","--labels","garbage_labels.txt","--input_layer","Placeholder","--output_layer","final_result","--image",imageURL]
            results = label.main(parameters)
            data = {results[0,0]:results[0,1],results[1,0]:results[1,1],results[2,0]:results[2,1],results[3,0]:results[3,1],results[4,0]:results[4,1],results[5,0]:results[5,1]}
            if app.debug:
                print(data)
            response, err = data,"error"
        else:
            return {'errorMessage': 'Please, provide a fileName...'}, 500
        if response:
            garbage_text = data
            return response, 200
        else:
            garbage_text = error
            return {'errorMessage': err}, 404

api.add_resource(Classification, '/classify')

@app.route('/')
def index():
    return render_template('webapp.html')

if __name__ == "__main__":
    app.run()