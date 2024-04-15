from flask import Flask, request, jsonify
from detect import getObjects
import cv2

app = Flask(__name__)

@app.route('/', methods=['GET'])
def check():
    return jsonify({'status': 'OK'})

@app.route('/upload', methods=['POST'])
def upload_image():
    if request.data:
        # Decode base64 image data
        image_data = request.data
        
        # Convert image data to NumPy array
        # nparr = np.frombuffer(image_data, np.uint8)
        
        # Decode image using OpenCV
        # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Display the image
        f = open('im.jpeg','wb')
        f.write(image_data)
        f.close()
        img = cv2.imread('im.jpeg')
        result, objectInfo = getObjects(img,0.45,0.2,objects=['elephant','zebra','bear'])
        if objectInfo != []:
            objectInfo[0][1]
            return objectInfo[0][1]

        # cv2.imshow('Uploaded Image',img )
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        return []
    else:
        return 'No image data provided'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
