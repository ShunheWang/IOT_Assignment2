from imutils.video import VideoStream
# from encode_utils import EncodePhoto
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import json

class FaceRecognition:
    """
    A class used to handle for facial recognization
    ...
    Methods
    -------
    loadEncodeData()
        execute the encode process
    initVideoStream()
        start video streaming
    closeVideoStream(vs)
        close video streaming
    run()
        execute the facial recognization process
    """    
    def __init__(self):
        """
        Parameters
        ----------
        encodings : str
            encoding filename
        detection_method : str
            detection method
        resolution : int
            resolution                                                                                      
        """
        with open("faceRecogniseConfig.json", "r") as file:
            data = json.load(file)
            self.encodings=data["encodings"]
            self.detection_method=data["detection_method"]
        self.resolution=240
        

    def loadEncodeData(self):
        # load the known faces and embeddings
        print("[INFO] loading encodings...")
        data = pickle.loads(open(self.encodings, "rb").read())
        return data

    def initVideoStream(self):
        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)
        return vs

    def closeVideoStream(self,vs):
        """
        Parameters
        ----------
        vs : object
           video streaming object                                                                                      
        """        
        print("[INFO] closing video stream...")
        vs.stop()
    
    def run(self):
        # self.encode.run()
        loadData=self.loadEncodeData()
        vs=self.initVideoStream()
        
        matchTimes=3
        print("You have 3 times chance to login")
        tempName="Unknown"
        while matchTimes>0:
            # grab the frame from the threaded video stream
            frame = vs.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width = self.resolution)

            boxes = face_recognition.face_locations(rgb, model = self.detection_method)
            encodings = face_recognition.face_encodings(rgb, boxes)
            
            # loop over the facial embeddings
            for encoding in encodings:
                matches = face_recognition.compare_faces(loadData["encodings"], encoding)
                #name = "Unknown"
                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    for i in matchedIdxs:
                        name = loadData["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                    tempName=max(counts, key = counts.get)
            
            # print to console, identified person
            print("Person found: {}".format(tempName))
            # Set a flag to sleep the cam for fixed time
            time.sleep(3.0)
            if tempName !="Unknown":
                self.closeVideoStream(vs)
                return tempName
            elif tempName =="Unknown":
                matchTimes-=1
                print("You have {} times chance to login".format(matchTimes))
        
        #close videoStream
        self.closeVideoStream(vs)
        
        return tempName