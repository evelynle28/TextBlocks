from flask import Flask, request, send_from_directory, abort, jsonify
import sqlite3
from inference import *
import os
import base64

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_OUTPUT_FOLDER = os.path.join(APP_ROOT, 'static')

app = Flask(__name__)

def save_image(bin_image, filename):
    absolute_path = os.path.join(IMG_OUTPUT_FOLDER, filename)
    cv2.imwrite(absolute_path, bin_image)

# # Return processed data from DB
# def get_image_data(image_id):
#     query = """ SELECT image_id, box_id, box_content, image_path
#                 FROM image_data WHERE image_id = '{}' """.format(str(image_id))

#     try:
#         conn = sqlite3.connect('img_database.db')
#         cur = conn.cursor()
#         cur.execute(query)
#         conn.commit()
#     except Exception as e:
#         print("Failed to load data: ", e)
#         conn.close()
#         return None
#     else:
#         results = cur.fetchall()
#         conn.commit()
#         conn.close()
#         return results

#NOTE: REQUEST!
@app.route('/upload', methods=['POST'])
def process_image():
    try:
        # convert string of image data to uint8
        nparr = np.frombuffer(request.data, np.uint8)
        # decode image
        bin_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print("start infering...")
        output_image_id, bin_output, box_data = perform_inference(bin_image)
        print("Done")
        # Save processed files for future references.
        output = output_image_id + '.png'
        save_image(bin_output, output)
        print(output + ' saved')

        # Convert to base64 encoding
        retval, buffer = cv2.imencode('.png', bin_output)
        base64_image = base64.b64encode(buffer).decode()

        return jsonify(
            id = output_image_id,
            blocks=box_data,
            img= base64_image
        ), 200
    except Exception as e:
        print(e)
        abort(500)


# @app.route('/images/:id', methods=['GET'])
# def get_image():
#     try:
#         return send_from_directory(IMG_OUTPUT_FOLDER, filename=output, as_attachment=True)
#     except FileNotFoundError:
#         abort(404)

# # @app.route('/data/:id')

app.run()
