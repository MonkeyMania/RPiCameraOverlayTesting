# Test Overlay Timer - has three overlays
import picamera
import time
from PIL import Image, ImageDraw, ImageFont

# Video Resolution
VIDEO_HEIGHT = 720
VIDEO_WIDTH = 1280

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)
fontBold = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf", 32)

textPad = Image.new('RGB', (1280, 64))
textPadImage = textPad.copy()

imgPad = Image.new('RGB', (1280, 299))
imgPadImage = imgPad.copy()

i = 0
with picamera.PiCamera() as camera:
   camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
   camera.framerate = 30
   camera.start_preview()
#   camera.wait_recording(0.9)

   racer1img = Image.open('racer1.jpg')
   racer2img = Image.open('racer2.jpg')
   racer3img = Image.open('racer3.jpg')

   racer1pad = Image.new('RGB', (
    ((racer1img.size[0] + 31) // 32) * 32,
    ((racer1img.size[1] + 15) // 16) * 16,
    ))
   racer2pad = Image.new('RGB', (
    ((racer2img.size[0] + 31) // 32) * 32,
    ((racer2img.size[1] + 15) // 16) * 16,
    ))
   racer3pad = Image.new('RGB', (
    ((racer3img.size[0] + 31) // 32) * 32,
    ((racer3img.size[1] + 15) // 16) * 16,
    ))

   racer1pad.paste(racer1img, (0, 0))
   racer2pad.paste(racer2img, (0, 0))
   racer3pad.paste(racer3img, (0, 0))

# Layer 3 top bar overlay
   overlay = camera.add_overlay(textPadImage.tobytes(), size=(1280, 64), alpha = 128, layer = 3, fullscreen = False, window = (0,20,1280,64))
   textPadImage = textPad.copy()
   drawTextImage = ImageDraw.Draw(textPadImage)
   drawTextImage.text((175, 18),"WEBELOS Round 2 Heat 01" , font=fontBold, fill=("Red"))
   overlay.update(textPadImage.tobytes())

# Layer 3 racer name bar overlay
   overlay = camera.add_overlay(textPadImage.tobytes(), size=(1280, 64), alpha = 128, layer = 3, fullscreen = False, window = (0,700,1280,64))
   textPadImage = textPad.copy()
   drawTextImage = ImageDraw.Draw(textPadImage)
   drawTextImage.text((50, 18),"Bob Schaefer" , font=fontBold, fill=("Yellow"))
   drawTextImage.text((300, 18),"Tim Schaefer" , font=fontBold, fill=("Yellow"))
   drawTextImage.text((550, 18),"Josie Schaefer" , font=fontBold, fill=("Yellow"))
   overlay.update(textPadImage.tobytes())

# Layer 3 racer pic bar overlay
   overlay = camera.add_overlay(racer1pad.tobytes(), size=racer1img.size, alpha = 255, layer = 3, fullscreen = False, window = (200,200,446,299))
   overlay = camera.add_overlay(racer2pad.tobytes(), size=racer2img.size, alpha = 255, layer = 3, fullscreen = False, window = (800,200,446,299))
   overlay = camera.add_overlay(racer3pad.tobytes(), size=racer3img.size, alpha = 255, layer = 3, fullscreen = False, window = (1400,200,446,299))

   camera.capture('test.jpg')

   try:
      while True:
         time.sleep(1)

   except KeyboardInterrupt:
      camera.remove_overlay(overlay)
      camera.stop_preview()

      print ("Cancelled")

   finally:
      camera.stop_preview()

print("end test")
