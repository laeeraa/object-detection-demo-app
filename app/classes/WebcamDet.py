from app.classes.VideoThread_OpenMMLab import VideoDetThread_OpenMMLab
from app.classes.ObjectDet import ObjectDet

from app.packages.Hand_Gesture_Recognizer.hand_gesture_detection import VideoDetThread
from threading import Event


class WebcamDet(ObjectDet): 

    def __init__(self):
        super().__init__()
        self.camera_id = 0
        self.api = "TechVidvan"
        self.stop_WebcamDetEvent = Event()

    
    def run(self, parent): 
        if (self.api == "TechVidvan"): 
            self.start_HandGestureRecog(parent)
        elif(self.api == "OpenMMLab"): 
            self.start_OpenMMLabDet(parent)
    
    
    def start_HandGestureRecog(self, parent): 
        self.stop_WebcamDetEvent.clear()
        # create the video capture thread
        self.thread = VideoDetThread(self.stop_WebcamDetEvent)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(parent.update_imageDet)
        # start the thread
        self.thread.start()

    def start_OpenMMLabDet(self, parent): 
        self.stop_WebcamDetEvent.clear() 
        self.thread = VideoDetThread_OpenMMLab(self, self.stop_WebcamDetEvent)
        self.thread.change_pixmap_signal.connect(parent.update_imageDet)
        self.thread.start()