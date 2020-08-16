from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import werkzeug, os, uuid, dlib, cv2

UPLOAD_FOLDER = 'img'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
parser = reqparse.RequestParser()
app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
keypoints = ['right_eye_0', 'right_eye_1', 'left_eye_2', 'left_eye_3', 'nose_4']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_landmarks(image_path, model_path):
    image = cv2.imread(image_path)
    face_detector = dlib.get_frontal_face_detector()
    dets = face_detector(image, 1)
    predictor = dlib.shape_predictor(model_path)
    result = []
    box = ['bounding box']
    result.append(box)
    for d in dets:
        box.append([d.left(), d.top(), d.right(), d.bottom()])
        cv2.rectangle(image, (d.left(), d.top()), (d.right(), d.bottom()), 255, 1)
        shape = predictor(image, d)
        for i in range(shape.num_parts):
            p = shape.part(i)
            result.append(keypoints[i])
            result.append([p.x, p.y])
        return result


class PhotoUpload(Resource):
    """Принимает фото методом POST"""

    def post(self):
        data = parser.parse_args()
        if data['file'] == "":
            return {
                'message': 'No file found',
                'status': 'error'
            }
        photo = data['file']
        if photo and allowed_file(photo.filename):
            filename = werkzeug.utils.secure_filename(photo.filename)
            extension = os.path.splitext(filename)[1]
            f_name = str(uuid.uuid4()) + extension
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
            data = get_landmarks(image_path=(os.path.join(app.config['UPLOAD_FOLDER'], f_name)),
                                 model_path='shape_predictor_5_face_landmarks.dat')
            return {
                'status': 'success',
                'points': data,
                'message': 'photo uploaded',
            }
        else:
            return {
                'message': 'Something when wrong',
                'status': 'error'
            }


api.add_resource(PhotoUpload, '/upload')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

