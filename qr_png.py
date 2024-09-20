#!/usr/bin/env python3
"""
QR Code Generator
Simple command-line program for generating QR codes with PNG file format.

NOTE: Using error correction constant ERROR_CORRECT_L may not be ideal when using an icon overlay. 
Perhaps use ERROR_CORRECT_H instead.

@date 2024.Sep.20
"""

import argparse
import getpass
import math
import qrcode
from PIL import Image, ImageDraw


def parse_args():
    parser = argparse.ArgumentParser(description="QR Code Generator")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-d', '--data', help="content to encode in the QR code")
    input_group.add_argument('-p', '--password', action='store_true', help="read content to encode in QR code from stdin")
    
    parser.add_argument('-q', '--qr-code', required=True, metavar="FILE", help="output QR code file name (omit extension)")
    parser.add_argument('-i', '--icon', required=False, metavar="FILE", help="overlay icon source file name")
    parser.add_argument('-s', '--scale', required=False, help="value to scale icon (percent)")
    parser.add_argument('-w', '--width', required=False, help="value to set icon width (pixels)")
    parser.add_argument('-v', '--version', help="version number to append to the file name")
    args = parser.parse_args()
    return args


def resize_scale(im:Image, scale:float) -> Image:
    return im.resize((int(im.size[0] * scale), int(im.size[1] * scale)))


def resize_ratio_w(im:Image, width:int) -> Image:
    """Adjust image width size and keep aspect ratio"""
    wpercent = (width/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    return im.resize((width, hsize), Image.LANCZOS)


def resize_ratio_h(im:Image, height:int) -> Image:
    """Adjust image height size and keep aspect ratio """
    wpercent = (height/float(im.size[1]))
    wsize = int((float(im.size[0])*float(wpercent)))
    return im.resize((wsize, height), Image.LANCZOS)


def gen_qr(qr_data:str, height=None) -> Image:
    """Generate QR code image from data string and resize to fit"""
    qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_code.add_data(qr_data)
    qr_code.make()
    qr_img = qr_code.make_image(fill_color='black', back_color="white").convert('1')
    if height is not None:
        qr_img = resize_ratio_h(qr_img, height)
    return qr_img


def overlay_icon(qr_img: Image, icon: Image, icon_scale: float = None, icon_width: int = None) -> Image:
    """ Overlay an icon image on the QR code image
        Optionally scale or resize the icon image
    """
    if icon_scale is not None and icon_width is not None:
        raise ValueError("Either icon_scale or icon_width must be None")
    elif icon_scale is not None:
        icon = resize_scale(icon, icon_scale)
    elif icon_width is not None:
        icon = resize_ratio_w(icon, icon_width)

    icon_pos = (
        (qr_img.size[0] - icon.size[0]) // 2,
        (qr_img.size[1] - icon.size[1]) // 2,
    )
    r = math.sqrt((icon.size[0]/2)**2 + (icon.size[1]/2)**2)
    draw = ImageDraw.Draw(qr_img)
    draw.ellipse(
        (
            (qr_img.size[0] / 2 - r, qr_img.size[1] / 2 - r),
            (qr_img.size[0] / 2 + r, qr_img.size[1] / 2 + r),
        ),
        fill='white',
    )
    qr_img.paste(icon, icon_pos, icon)
    return qr_img


if __name__ == "__main__":
    args = parse_args()
    
    qr_data = None
    if args.data is not None:
        qr_data = args.data
    elif args.password is not None:
        qr_data = getpass.getpass()
    else:
        # Note: we should never get here!
        raise ValueError("Invalid input arguments")
    
    v = f'-{args.version}' if args.version else ''
    qr_fname = f'{args.qr_code}{v}.png'
    qr = gen_qr(qr_data)

    if args.icon:
        overlay_icon(qr, Image.open(args.icon), icon_scale=float(args.scale) if args.scale else None, icon_width=int(args.width) if args.width else None)

    qr.save(qr_fname)
    print(f"QR code generated: \n  {qr_fname}")
