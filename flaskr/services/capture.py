from .. import face_recognition
from .. import mongo
from .. import np
from .. import os
from .. import app
from .. import DISTANCE
from .. import WAIT_TIME
from .. import SOURCE_FOLDER
from .. import time


def get_image_encoding_path():
    image_encoding_file_name = 'enc.npy'
    image_encoding_file_path = os.path.join(app.root_path, 
                                            SOURCE_FOLDER,  
                                            image_encoding_file_name)
    return image_encoding_file_path


def get_image_encoding_array(image_encoding):
    return np.array(image_encoding)


def get_all_image_encodings(image_encoding_file_path):
    return np.load(image_encoding_file_path, allow_pickle=True)


def calculate_distance_vector(all_image_encodings, image_encoding):
    return np.sqrt(np.sum((all_image_encodings - image_encoding) ** 2, axis=1))


def calculate_smallest_dictance_value(array):
    return np.amin(array)


def calculate_smallest_distance_value_index(array, value):
    smallest_value_indexes = np.where(array == value)

    if smallest_value_indexes and smallest_value_indexes[0].size != 0:
            smallest_value_index = int(smallest_value_indexes[0][0])

            return smallest_value_index

    return False


def find_user_by_image_index(index):
    return mongo.db.users.find_one({'image_indexes': index}, sort=[('created', -1)])


def find_capture_by_user_id(id):
    return mongo.db.captures.find_one({'user_id': id}, sort=[('created', -1)])


def create_capture(description, user, created):
    capture = {
        'description': description,
        'user_id': user.get('_id'),
        'created': created
    }

    mongo.db.captures.insert(capture)

    capture['id'] = str(capture.pop('_id'))
    capture['user_id'] = str(capture.pop('user_id'))

    return capture


def create(data):
    description = data.get('description')
    image_encoding = data.get('image_encoding')
    now = time.time()
    found_user = None

    image_encoding_array = get_image_encoding_array(image_encoding)
    image_encoding_file_path = get_image_encoding_path()

    if os.path.exists(image_encoding_file_path):
        all_image_encodings = get_all_image_encodings(image_encoding_file_path)
        distance_vector = calculate_distance_vector(all_image_encodings, image_encoding_array)
        smallest_distance_value = calculate_smallest_dictance_value(distance_vector)
        smallest_distance_value_index = calculate_smallest_distance_value_index(distance_vector, smallest_distance_value)

        found_user = find_user_by_image_index(smallest_distance_value_index)

    if found_user:
        found_user_id = found_user.get('_id')
        previous_capture = find_capture_by_user_id(found_user_id)

        if previous_capture:
            created_time_left = now - previous_capture.get('created')

            if created_time_left > WAIT_TIME:
                return create_capture(description, found_user, now)

            else:
                return {
                    'description': 'User was already captured'
                }

        else:
            return create_capture(description, found_user, now)

    return None