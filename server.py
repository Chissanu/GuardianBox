from flask import Flask, Response, request
import cv2
import time
import numpy as np
import os
import nextcloud_client
from dotenv import dotenv_values
import requests
from datetime import datetime

app = Flask(__name__)
# config = dotenv_values(".env")

# nc = nextcloud_client.Client(config['NC_URL'])
# nc.login(config['NC_USER'], config['NC_PASS'])
nc = None
root_nc_dir = "CCTV/"

recording_cam_1 = False
recording_cam_2 = False
recording_cam_3 = False

stop_cam_1 = False
stop_cam_2 = False
stop_cam_3 = False

# This function will always run and will stream the camera output alongside taking videos
def camera_1_feed():
    global recording_cam_1
    global stop_cam_1
    video_index = 0
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0)
    vs.set(cv2.CAP_PROP_FPS, 10)
    vs.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video_frames = []
    while True:
        currTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ret, frame = vs.read()
        if recording_cam_1 == True:
            video_frames.append(frame)
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        print(currTime + " Camera 1 Recording: ", recording_cam_1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if recording_cam_1 == False and len(video_frames) > 0:
            output_file = f'cam_0_clip_{video_index}.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_file, fourcc, 10.0, (640, 480))
            for frame in np.array(video_frames):
                out.write(frame)
            video_frames = []
            if video_index >= 5:
                video_index = 0
            else:
                video_index += 1
            
            nc_dir = root_nc_dir + output_file
            nc.put_file(nc_dir, output_file)
            print("Video Wrote")
            out.release()

        if stop_cam_1 == True:
            break
    vs.release()
    cv2.destroyAllWindows()

def camera_2_feed():
    global recording_cam_2
    global stop_cam_2
    video_index = 0
    """Video streaming generator function."""
    vs = cv2.VideoCapture(2)
    vs.set(cv2.CAP_PROP_FPS, 10)
    vs.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video_frames = []
    while True:
        currTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ret, frame = vs.read()
        if recording_cam_2 == True:
            video_frames.append(frame)
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        print(currTime + " Camera 2 Recording: ", recording_cam_2)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if recording_cam_2 == False and len(video_frames) > 0:
            output_file = f'cam_2_clip_{video_index}.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_file, fourcc, 10.0, (640, 480))
            for frame in np.array(video_frames):
                out.write(frame)
            video_frames = []
            if video_index >= 5:
                video_index = 0
            else:
                video_index += 1
            
            nc_dir = root_nc_dir + output_file
            nc.put_file(nc_dir, output_file)
            print("Video Wrote")
            out.release()

        if stop_cam_2 == True:
            break

    vs.release()
    cv2.destroyAllWindows()

def camera_3_feed():
    global recording_cam_3
    global stop_cam_3
    video_index = 0
    """Video streaming generator function."""
    vs = cv2.VideoCapture(4)
    vs.set(cv2.CAP_PROP_FPS, 10)
    vs.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video_frames = []
    while True:
        currTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ret, frame = vs.read()
        if recording_cam_3 == True:
            video_frames.append(frame)
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        print(currTime + " Camera 3 Recording: ", recording_cam_2)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if recording_cam_3 == False and len(video_frames) > 0:
            output_file = f'cam_3_clip_{video_index}.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_file, fourcc, 10.0, (640, 480))
            for frame in np.array(video_frames):
                out.write(frame)
            video_frames = []
            if video_index >= 5:
                video_index = 0
            else:
                video_index += 1
            
            nc_dir = root_nc_dir + output_file
            nc.put_file(nc_dir, output_file)
            print("Video Wrote")
            out.release()

        if stop_cam_3 == True:
            break

    vs.release()
    cv2.destroyAllWindows()

@app.route('/camera-1')
def cam1():
    """Video streaming route for camera 1."""
    global stop_cam_1
    stop_cam_1 = False
    return Response(camera_1_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-1/stop')
def stopCam1():
    global stop_cam_1
    stop_cam_1 = True
    return "Camera 1 Stopped"

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
    global stop_cam_2
    stop_cam_2 = False
    return Response(camera_2_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-2/stop')
def stopCam2():
    global stop_cam_2
    stop_cam_2 = True
    return "Camera 2 Stopped"

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

@app.route('/camera-3')
def cam3():
    """Video streaming route for camera 3."""
    global stop_cam_3
    stop_cam_3 = False
    return Response(camera_3_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-3/stop')
def stopCam3():
    global stop_cam_3
    stop_cam_3 = True
    return "Camera 3 Stopped"

@app.route('/camera-3/start-record')
def recordCam3():
    global recording_cam_3
    recording_cam_3 = True
    return "Recording Started"

@app.route('/camera-3/stop-record')
def stopRecordCam3():
    global recording_cam_3
    recording_cam_3 = False
    return "Recording Stopped"

@app.route('/configure-nextcloud', methods=['POST'])
def configureNextcloud():
    global nc
    data = request.json
    try:
        nc = nextcloud_client.Client(data['url'])
        nc.login(data['username'], data['password'])
        root_nc_dir = data['directory']
        print("Nextcloud Configured")
        return "Nextcloud Configured Successfully"
    except:
        print("Nextcloud Configuration Failed")
        return "Nextcloud Configuration Failed, Check Credentials and URL"
    
@app.route('/test-request')
def testRequest():
    return "Request Successful"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
