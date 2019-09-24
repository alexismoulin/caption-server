""" Caption Server"""
# pylint: disable-msg=C0103
from flask import Flask, request
from flask_restful import Api, Resource
from functions import save_image, greedy_search

# Setup the folder where the images will be uploaded
UPLOAD_FOLDER = './image'

#Lanch the flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

api = Api(app=app)

class Endpoint(Resource):
    """ Endpoint containing only 2 HTTP methods:
        GET - only for testing purpose
        POST - getting an image from the client
        and returning a json object with the caption of the image
    """
    def get(self):
        """ For testing purpose only """
        return "OK - Server is working", 200

    def post(self):
        """ Receive image data from client and returns a caption of the image """
        if request.files:
            img = request.files['image']
            save_image(img)
            response = greedy_search("./image/test.jpg")
            return response, 200
        else:
            return {"message": "Error - wrong file posted"}, 400


api.add_resource(Endpoint, "/endpoint")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
