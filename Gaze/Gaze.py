import time
from threading import Thread
import cv2

#ptgaze part way more detailed and compliicated but probably worth it
#https://pypi.org/project/ptgaze/
import ptgaze as pg
from ptgaze import main as pgm
from ptgaze import utils as pgu
from ptgaze import gaze_estimator

#is it working? yes, is it working well? ...no
class GazeEvaluator():
    _FPS=3
    _running=True
    _loop=None
    _calibration=[]
    _calibrating=False
    _hor_Range=[-0.5,0.5]
    _ver_Range=[-0.6,0.0]

    text=""
    
    def __init__(self):
        ag=pgm.parse_args()
        ag.mode = 'eth-xgaze'
        conf=pgm.load_mode_config(ag)
        pgu.expanduser_all(conf)
        
        self.reset()
        self.gz= gaze_estimator.GazeEstimator(conf)
        self.cam = cv2.VideoCapture(0)

    def evaluate(self,img):
        faces=self.gz.detect_faces(img)
        temp=0
        if faces:
            self.gz.estimate_gaze(img,faces[0])
            ta=faces[0].normalized_gaze_angles
            if self._calibrating:
                self._calibration.append(ta)
            if ta[0]<=self._ver_Range[1] and ta[0]>=self._ver_Range[0] and ta[0]<=self._ver_Range[1] and ta[0]>=self._ver_Range[0]:
                temp=1
            
        self._attention=(self._attention[0]+temp,self._attention[1]+1)

    def reset(self):
        self._attention=(0,0)

    def getAttention(self):
        if self._attention[1]==0:
            return 1
        return self._attention[0]/self._attention[1]

    def getCalibration(self):
        return self._calibration

    def run(self):
        self._running=True
        self._loop=Thread(target=self._looping)
        self._loop.start()

    def stop(self):
        self._running=False
        self._loop.join()
        self._loop=None
        
    def _looping(self):
        while self._running:
            _, img=self.cam.read()
            st=time.time()
            self.evaluate(img)
            et=time.time()
            if (et-st) < 1/self._FPS:
                time.sleep((1/self._FPS)-(et-st))

if __name__=="__main__":
    eval=GazeEvaluator()
    eval.reset()
    eval.run()
    time.sleep(10)
    res=eval.getAttention()
    print(res)
    eval.stop()

