# Reference: reference the source code from tutorial provide from RMIT 

from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2

class barcodeScan:
    """
    A class used to handle barcode scanning
    ...
    Methods
    -------
    initVideoStream()
        start video streaming
    closeVideoStream()
        close video streaming 
    run() 
        start the program        
    """
    def initVideoStream(self):
        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)
        return vs

    def closeVideoStream(self,vs):
        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] closing video stream...")
        vs.stop()

    def run(self):
        vs=self.initVideoStream()
        #found = set()

        while True:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width = 400)
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)
            if len(barcodes):
                barcodeData = barcodes[0].data.decode("utf-8")
                barcodeType = barcodes[0].type
            # if the barcode text has not been seen before print it and update the set
            # if barcodeData not in found:
                print("[FOUND] Type: {}, Data: {}".format(barcodeType, barcodeData))
                self.closeVideoStream(vs)
                return barcodeData
                
            # wait a little then close video resources
            time.sleep(1)

#barcodeScanReturnBooks().run()
