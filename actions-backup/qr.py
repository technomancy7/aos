import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import pyzbar.pyzbar as pyzbar
from pyzbar.pyzbar import ZBarSymbol
from PIL import Image

def action_data():
    return {
        "name": "qr",
        "author": "Kaiser",
        "version": "0.0",
        "features": [],
        "group": "system",
}

def on_help(ctx):
    return """   

    Commands:
        parse | read <source>
            Attempts to read a QR code.
            Source can be a path to an image file, or "camera" to use webcam.
            Camera is default if no image path is given.

        create | make <text>
            Creates a qr code from the text given.
            File is saved in action data directory as `qrcode.png`


    """
def parse_qr(ctx, source):
    out = []
    if source == "camera":
        camera = ctx.quick_run("camera capture")
        source = camera.data_path()+"webcam.png"

    input_image = Image.open(source)

    decoded_objects = pyzbar.decode(input_image, symbols=[ZBarSymbol.QRCODE])
    for obj in decoded_objects:
        zbarData = obj.data.decode("utf-8")
        out.append(zbarData)
    return out

def create_qr(ctx, text):
    fill_colour = ctx.touch_config("qr.fill_colour", "blue")
    back_colour = ctx.touch_config("qr.back_colour", "black")
    outpath = f"{ctx.data_path()}qrcode.png"
    img = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_L)
    img.add_data(text)
    img2 = img.make_image(fill_color=fill_colour, back_color=back_colour)
    img2.save(outpath)
    return outpath

def on_load(ctx): 
    cmd = ctx.get_string_ind(0)
    
    match cmd:
        case "parse" | "read":
            src = ctx.get_string()[len(cmd)+1:] or "camera"
            p = parse_qr(ctx, src)
            print(p)
        
        case "make" | "create" | "m" | "c":
            p = create_qr(ctx, ctx.get_string()[len(cmd)+1:])
            ctx.view_image(p)

    return ctx
