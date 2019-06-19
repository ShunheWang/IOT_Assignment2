from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import json

class EncodePhoto:
    """
    A class used to encode photo for facial recognization
    ...
    Methods
    -------
    run()
        execute the encode process
    """    
    def __init__(self):
        """
        Parameters
        ----------
        dataset : str
           photo file path
        encodings : str
            encoding filename
        detection_method : str
            detection method
        knownEncodings : str
            encoding
        knownNames : str
            name                                                                                      
        """ 
        with open("faceRecogniseConfig.json", "r") as file:
            data = json.load(file)
            self.dataset = data["dataset"]
            self.encodings=data["encodings"]
            self.detection_method=data["detection_method"]
        # initialize the list of known encodings and known names
        self.knownEncodings = []
        self.knownNames = []
    
    def run(self):
        # grab the paths to the input images in our dataset
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images(self.dataset))

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]
            print("name: "+name)
            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model = self.detection_method)

            # compute the facial embedding for the face
            computeEncodings = face_recognition.face_encodings(rgb, boxes)
            
            # loop over the encodings
            for encoding in computeEncodings:
                # add each encoding + name to our set of known names and encodings
                self.knownEncodings.append(encoding)
                self.knownNames.append(name)
        
        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = { "encodings": self.knownEncodings, "names": self.knownNames }

        with open(self.encodings, "wb") as f:
            f.write(pickle.dumps(data))