# Test Overlay Timer - has three overlays
import picamera
import time
from PIL import Image, ImageDraw, ImageFont

# Video Resolution
VIDEO_HEIGHT = 480
VIDEO_WIDTH = 640

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)
fontBold = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf", 32)

textPadSideBar = Image.new('RGB', (224, 960))
textPadSideBarImage = textPadSideBar.copy()

textPadNameBar = Image.new('RGB', (1920, 64))
textPadNameBarImage = textPadNameBar.copy()

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

# Layer 3 left bar overlay
    textPadImageLeft = textPadSideBar.copy()
    drawTextImage = ImageDraw.Draw(textPadImageLeft)
    drawTextImage.text((20, 20),"Webelos" , font=fontBold, fill=("Red"))
    overlayleft = camera.add_overlay(textPadImageLeft.tobytes(), size=(224, 960), alpha = 255, layer = 3, fullscreen = False, window = (0,0,224,960))

    textPadImageRight = textPadSideBar.copy()
    drawTextImage = ImageDraw.Draw(textPadImageRight)
    drawTextImage.text((20, 20),"Race 1" , font=fontBold, fill=("Yellow"))
    drawTextImage.text((20, 200),"Heat 1 of 6" , font=fontBold, fill=("Yellow"))
    overlayright = camera.add_overlay(textPadImageRight.tobytes(), size=(224, 960), alpha = 255, layer = 3, fullscreen = False, window = (1696,0,224,960))

# Layer 3 racer name bar overlay
    textPadImageNames = textPadNameBar.copy()
    drawTextImage = ImageDraw.Draw(textPadImageNames)
    drawTextImage.text((300, 18),"Bob Schaefer" , font=fontBold, fill=("Yellow"))
    drawTextImage.text((900, 18),"Tim Schaefer" , font=fontBold, fill=("Yellow"))
    drawTextImage.text((1400, 18),"Josie Schaefer" , font=fontBold, fill=("Yellow"))
    overlaynames = camera.add_overlay(textPadImageNames.tobytes(), size=(1920, 64), alpha = 255, layer = 3, fullscreen = False, window = (0,1016,1920,64))

# Layer 3 racer pic bar overlay
    overlay = camera.add_overlay(racer1pad.tobytes(), size=racer1img.size, alpha = 255, layer = 3, fullscreen = False, window = (200,700,446,299))
    overlay = camera.add_overlay(racer2pad.tobytes(), size=racer2img.size, alpha = 255, layer = 3, fullscreen = False, window = (800,700,446,299))
    overlay = camera.add_overlay(racer3pad.tobytes(), size=racer3img.size, alpha = 255, layer = 3, fullscreen = False, window = (1300,700,446,299))

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
