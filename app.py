from flask import Flask, request
from flask_restful import Resource, Api
from audio_compare import get_distance, load_all

class IdentifyAlphabet(Resource):
    def __init__(self, *args, **kwargs):
        super(IdentifyAlphabet, self).__init__()
        # load_all()
        
    def post(self):
        if request.files:
            file = request.files['file']
            file.save('/tmp/%s' %file.filename)
            alphabet = request.args.get('alphabet')
            if alphabet:
                data = get_distance(alphabet, '/tmp/%s' %file.filename)
                new_data = []
                for key in data:
                    new_data.append({'key': key, 'value': data[key]})
                return sorted(new_data, key=lambda x: x['value'])                        
            else:
                return {'msg': 'missing reference alphabet'}
        return {'msg': 'missing audio file'}

def prepare():
    load_all()

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(IdentifyAlphabet, '/12khadi')
   
    load_all()
    app.run('0.0.0.0', debug=True)
