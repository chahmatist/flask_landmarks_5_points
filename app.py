from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import werkzeug, os, uuid, dlib, cv2

UPLOAD_FOLDER = 'img'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
POINTS_TEXT = ['right_eye_0', 'right_eye_1', 'left_eye_2', 'left_eye_3', 'nose_4']
parser = reqparse.RequestParser()
app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_landmarks(image_path, model_path):
    image = cv2.imread(image_path)
    face_detector = dlib.get_frontal_face_detector()
    dets = face_detector(image, 1)
    predictor = dlib.shape_predictor(model_path)
    result = []
    for d in dets:
        result.append({'bounding box': {"left": d.left(), "top": d.top(), "right": d.right(), "bottom": d.bottom()}})
        cv2.rectangle(image, (d.left(), d.top()), (d.right(), d.bottom()), 255, 1)
        shape = predictor(image, d)
        for i in range(shape.num_parts):
            p = shape.part(i)
            result.append({POINTS_TEXT[i]: {"x": p.x, "y": p.y}})
        return result


class PhotoUpload(Resource):
    """Принимает фото методом POST"""

    def post(self):
        data = parser.parse_args()
        if data['file'] == "":
            return {
                'message': 'Фото не получено, поорпбуйте еще раз',
                'status': 'Ошибка'
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
                'points': data,
                'message': 'Фото получено',
                'status': 'Успех'
            }
        else:
            return {
                'message': "что-то пошло не так! фото должно содержать (фронтальное изображение лица человека в формате 'jpg' или 'jpeg')",
                'status': 'Ошибка'
            }


api.add_resource(PhotoUpload, '/upload')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
