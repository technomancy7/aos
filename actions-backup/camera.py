import os, json, subprocess, shutil
import time
import cv2

def action_data():
    return {
        "name": "camera",
        "author": "Kaiser",
        "version": "0.0",
        "features": [],
        "group": "system",
}
open_file_name = ""

def on_help(ctx):
    return """   

    Commands:
        capture [delay]
            Captures an image from the webcam after [delay] seconds and saves it in action data directory.

    """
def capture_webcam(ctx, *, camera = 0, delay = 0.1):
    p = ctx.data_path()+"webcam.png"
    camera_port = camera
    camera = cv2.VideoCapture(camera_port)
    time.sleep(delay)  # If you don't wait, the image will be dark
    _, image = camera.read()
    cv2.imwrite(p, image)
    del(camera)  # so that others can use the camera as soon as possible
    return p

def on_load(ctx): 
    apps_dir = ctx.data_path()
    if not os.path.exists(apps_dir):
        os.mkdir(apps_dir)

    cmd = ctx.get_string_ind(0)
    line = ""
    if len(ctx.get_string_list()) > 1:
        line = ctx.get_string_list()[1]
    
    match cmd:
        case "capture" | "c":
            delay = 0.1
            try:
                delay = float(line)
            except: pass

            p = capture_webcam(ctx, delay = delay)
            ctx.say("Capture taken from web cam.")
            ctx.view_image(p)
    return ctx
