from flask import Flask, Response
import cv2
import time
import numpy as np
import os
import nextcloud_client
from dotenv import dotenv_values
import requests

app = Flask(__name__)
config = dotenv_values(".env")

nc = nextcloud_client.Client(config['NC_URL'])
nc.login(config['NC_USER'], config['NC_PASS'])
recording_cam_1 = False
recording_cam_2 = False

# This function will always run and will stream the camera output alongside taking videos
def camera_1_feed():
    global recording_cam_1
    video_index = 0
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0)
    vs.set(cv2.CAP_PROP_FPS, 10)
    video_frames = []
    while True:
        ret, frame = vs.read()
        if recording_cam_1 == True:
            video_frames.append(frame)
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        print("Camera 1 Recording: ", recording_cam_1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if recording_cam_1 == False and len(video_frames) > 0:
            output_file = f'cam_0_clip_{video_index}.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))
            for frame in np.array(video_frames):
                out.write(frame)
            video_frames = []
            if video_index >= 5:
                video_index = 0
            else:
                video_index += 1
            
            nc_dir = "CCTV/" + output_file
            nc.put_file(nc_dir, output_file)
            print("Video Wrote")
            out.release()

    vs.release()
    cv2.destroyAllWindows()

def camera_2_feed():
    global recording_cam_2
    video_index = 0
    """Video streaming generator function."""
    vs = cv2.VideoCapture(2)
    vs.set(cv2.CAP_PROP_FPS, 10)
    video_frames = []
    while True:
        ret, frame = vs.read()
        if recording_cam_2 == True:
            video_frames.append(frame)
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        print("Camera 2 Recording: ", recording_cam_2)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if recording_cam_2 == False and len(video_frames) > 0:
            output_file = f'cam_2_clip_{video_index}.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))
            for frame in np.array(video_frames):
                out.write(frame)
            video_frames = []
            if video_index >= 5:
                video_index = 0
            else:
                video_index += 1
            
            nc_dir = "CCTV/" + output_file
            nc.put_file(nc_dir, output_file)
            print("Video Wrote")
            out.release()

    vs.release()
    cv2.destroyAllWindows()

@app.route('/camera-1')
def cam1():
    """Video streaming route for camera 1."""
    return Response(camera_1_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-1/start-record')
def recordCam1():
    global recording_cam_1
    recording_cam_1 = True
    return "Recording Started"

@app.route('/camera-1/stop-record')
def stopRecordCam1():
    global recording_cam_1
    recording_cam_1 = False
    return "Recording Stopped"

@app.route('/camera-2')
def cam2():
    """Video streaming route for camera 2."""
    return Response(camera_2_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-2/start-record')
def recordCam2():
    global recording_cam_2
    recording_cam_2 = True
    return "Recording Started"

@app.route('/camera-2/stop-record')
def stopRecordCam2():
    global recording_cam_2
    recording_cam_2 = False
    return "Recording Stopped"

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
