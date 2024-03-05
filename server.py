from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def cameraFeed(camera_index):
    """Video streaming generator function."""
    vs = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = vs.read()
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    vs.release()
    cv2.destroyAllWindows() 

@app.route('/camera-1')
def cam_1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(cameraFeed(0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-2')
def cam_2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(cameraFeed(2), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-3')
def cam_3():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(cameraFeed(4), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-4')
def cam_4():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(cameraFeed(6), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
