# Test Overlay Timer - has three overlays
import picamera
import time
from PIL import Image, ImageDraw, ImageFont
import pygame.display

# Video Resolution
VIDEO_HEIGHT = 480
VIDEO_WIDTH = 640

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)
fontBold = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf", 48)

# function for toggling the screen to be blanked or not - here due to repeated use      
def HideTheDesktop(hideIt = True):
    if hideIt:
        #set blank screen behind everything
        pygame.display.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill((0, 0, 0))
    else:
        pygame.display.quit()

textPad = Image.new('RGB', (224, 960))
textPadImage = textPad.copy()

imgPad = Image.new('RGB', (224, 224))
imgPadImage = imgPad.copy()

denimage = Image.open('webelos.png')

denpad = Image.new('RGB', (
 ((denimage.size[0] + 31) // 32) * 32,
 ((denimage.size[1] + 15) // 16) * 16,
 ))

denpad.paste(denimage, (0, 0))

with picamera.PiCamera() as camera:
    camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
    camera.vflip = False
    camera.hflip = True
    camera.framerate = 90
    camera.exposure_mode = 'sports'
    camera.iso = 0
    HideTheDesktop(True)
    camera.start_preview()
#    camera.wait_recording(0.9)

     #Setup overlays and show them
    textPadImageLeft = textPad.copy()
    drawTextImage = ImageDraw.Draw(textPadImageLeft)
    drawTextImage.text((20, 20),"Webelos" , font=fontBold, fill=("Red"))
    overlayleft = camera.add_overlay(textPadImageLeft.tobytes(), size=(224, 960), alpha = 255, layer = 3, fullscreen = False, window = (0,0,224,960))

    textPadImageRight = textPad.copy()
    drawTextImage = ImageDraw.Draw(textPadImageRight)
    drawTextImage.text((20, 20),"Round3" , font=fontBold, fill=("Yellow"))
    drawTextImage.text((20, 200),"Heat01" , font=fontBold, fill=("Yellow"))
    overlayright = camera.add_overlay(textPadImageRight.tobytes(), size=(224, 960), alpha = 255, layer = 3, fullscreen = False, window = (1696,0,224,960))

    overlay = camera.add_overlay(denpad.tobytes(), size=denimage.size, alpha = 255, layer = 3, fullscreen = False, window = (0,400,224,224))

    lastcheckin = time.time()

    running = True
    try:
        while running:
            time.sleep(1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if time.time() > (lastcheckin + 30):
                running = False
                    
        HideTheDesktop(False)

    finally:
        camera.remove_overlay(overlayleft)
        camera.remove_overlay(overlayright)
        camera.stop_preview()
        HideTheDesktop(False)
        print("end test")
