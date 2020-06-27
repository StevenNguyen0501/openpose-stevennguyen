from flask import Flask
# from flask_restplus import Resource, Api, reqparse

from flask_restful import Resource, Api, reqparse
from examples.apis.pose_key_points_from_image_api import get_25_key_points
from examples.apis.utils import is_the_pose_valid

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Human25KeyPoints(Resource):
    def post(self):
        parser.add_argument('personURL', type=str)
        args = parser.parse_args()
        key_points = get_25_key_points(args['personURL'])

        message, is_valid, key_points = is_the_pose_valid(key_points)

        return {
            "status": is_valid,
            "message": message,
            "key_points": str(key_points)
        }


api.add_resource(Human25KeyPoints, '/openpose_caffe')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000, threaded=True)
