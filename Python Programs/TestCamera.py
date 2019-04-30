from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.image_effect = 'denoise'
camera.image_effect = 'colorbalance'
camera.image_effect = 'colorpoint'
camera.image_effect = 'saturation'
sleep(30)
camera.stop_preview()
