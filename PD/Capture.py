#!/usr/bin/env python
"""Plant Detection Image Capture.

For Plant Detection.
"""
import sys, os
import numpy as np
import cv2
import platform
from time import sleep
from datetime import datetime
from gi.repository import GExiv2

use_rpi_camera = False
using_rpi = False

if platform.uname()[4].startswith("arm"):
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    using_rpi = True

class Capture():
    """Capture image for Plant Detection"""
    def __init__(self, **kwargs):
        self.image = None
        self.ret = None
        self.camera_port = 0
        self.timestamp = datetime.now().isoformat()
        self.current_coordinates = None
        self.test_coordinates = [2000, 2000]
        self.output_text = True

    def _getcoordinates(self):
        """Get machine coordinates from bot."""
        # For now, return testing coordintes:
        return self.test_coordinates

    def capture(self):
        """Take a photo."""
        if using_rpi and use_rpi_camera:
            # With Raspberry Pi Camera:
            with PiCamera() as camera:
                camera.resolution = (1920, 1088)
                rawCapture = PiRGBArray(camera)
                sleep(0.1)
                camera.capture(rawCapture, format="bgr")
                self.image = rawCapture.array
        else:
            # With USB cameras:
            camera = cv2.VideoCapture(0)
            sleep(0.1)
            camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1600)
            camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1200)
            self.ret, self.image = camera.read()
            camera.release()
        if not self.ret:
            raise IOError("No camera detected.")
        return self.image

if __name__ == "__main__":
    from Image import Image
    image = Capture().capture()
    wimage = Image()
    wimage.image = image
    wimage.save('capture')

    exif = GExiv2.Metadata('capture.jpg')
    current_coordinates = Capture()._getcoordinates()
    timestamp = Capture().timestamp
    exif['Exif.Image.ImageDescription'] = 'Coordinates: {}, Timestamp: {}'.format(
                                          current_coordinates, timestamp)
    print(exif.get_comment())
    exif.save_file()