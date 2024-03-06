from flask import Flask, Response
import cv2
import time
import numpy as np

app = Flask(__name__)

# This function will always run and will stream the camera output alongside taking videos
def camera_feed(camera_index):
    video_index = 0
    """Video streaming generator function."""
    vs = cv2.VideoCapture(camera_index)
    start_time = time.time()
    video_frames = []
    while True:
        ret, frame = vs.read()
        video_frames.append(frame)
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if time.time() - start_time > 30:
            output_file = f'cam_{camera_index}_clip_{video_index}.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))
            for frame in np.array(video_frames):
                out.write(frame)
            video_frames = []
            start_time = time.time()
            if video_index > 10:
                video_index = 0
            else:
                video_index += 1
            out.release()

    vs.release()
    cv2.destroyAllWindows() 

@app.route('/camera-1')
def cam_1():
    global cam_1_vindex
    """Video streaming route for camera 1."""
    return Response(camera_feed(0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-2')
def cam_2():
    global cam_2_vindex
    """Video streaming route for camera 2."""
    return Response(camera_feed(2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
