from flask import Flask, request, send_from_directory, abort, jsonify
from inference import *
import os
import base64
import traceback

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_OUTPUT_FOLDER = os.path.join(APP_ROOT, 'static')

app = Flask(__name__)

def save_image(bin_image, filename):
    absolute_path = os.path.join(IMG_OUTPUT_FOLDER, filename)
    cv2.imwrite(absolute_path, bin_image)


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
        print(str(e))
        traceback.print_exec()
        abort(500)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'success', 200

app.run(host="172.31.27.145", port=5000)
