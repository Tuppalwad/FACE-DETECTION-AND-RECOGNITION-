from flask import Flask, jsonify, render_template, make_response,Response
from flask_cors import CORS, cross_origin
from camera import Video
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

def gen_name(camera): 
    jpg,frame=camera.get_frame()
    return camera.get_name_of_person(frame)
def gen(camera):
    while True:
        jpg,frame=camera.get_frame()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'+ jpg +
                b'\r\n\r\n') 
def stop_cam(camera):
    camera.__del__()
@app.route("/video")       
def video():
    path='Images'
    return Response(gen(Video(path)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route("/name")
def name():
    path="images"
    n=gen_name(Video(path))
    return n


@app.route('/')
@app.route('/index')
@cross_origin()
def index():
    resp = make_response(render_template('index.html', active_page="home"))
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp


@app.route('/Name')
def components():
    return render_template('Name.html', active_page="name")

if __name__=='__main__':
    app.run(debug=True)