# Converts images into a ROM cell containing signals for the 256x128 rail screen.
import argparse
import json
import blueprint
import cv2
import numpy as np
from bitstring import BitArray
from PIL import Image

WIDTH = 256
HEIGHT = 128
assert HEIGHT % 4 == 0


def main(img):
    bp = blueprint.Blueprint.from_exchange_string(
        '0eNptjsEKwjAQRP9lzhGspInNr4hIq4sstNvSbMVS8u828eLB28yw82Y3dP1C08yiCBv4PkpEuGyI/JS2z5muEyGAlQYYSDtkF5cuaqs8CpIBy4PeCFW6GpAoK9OXUsx6k2XoaN4P/vUNpjFykfvajjnU1hqsCLVrUkaW6fDzqcGL5lgap3NlvW2889XR1S6lD4zTRSo=')
    bp.data['blueprint']['entities'] = []
    with open('signal_names.json') as f:
        SIGNALS = json.load(f)

    img = img.resize((WIDTH, HEIGHT))
    image = img.convert('1')

    # og_image = cv2.imread(image_path)
    # og_image = cv2.resize(og_image, dsize=(WIDTH, HEIGHT))
    # gr_image = cv2.cvtColor(og_image, cv2.COLOR_BGR2GRAY)
    # threshold = np.average([gr_image[i, j] for i in range(HEIGHT) for j in range(WIDTH)])
    # _, image = cv2.threshold(gr_image, 127, 255, cv2.THRESH_BINARY)

    for i in range(0, HEIGHT // 32):
        integer_segment = []
        combinators = [{
            'entity_number': i * 18 + x,
            'name': 'constant-combinator',
            'position': {
                'x': x + 0.5,
                'y': i + 0.5
            },
            'control_behavior': {
                'filters': []
            }
        } for x in range(15)]
        for j in range(0, 256):
            column_integer = [0] * 32
            for k in range(0, 32):
                # pixel = 1 if image[i * 32 + 32 - k - 1, j] == 255 else 0
                pixel = 1 if image.getpixel((j, i * 32 + 32 - k - 1)) == 255 else 0
                column_integer[31-k] = pixel
            integer_segment.append(BitArray(bin=''.join(map(str, column_integer))).int)
        for l, signal in enumerate(SIGNALS):
            combinators[l // 18]['control_behavior']['filters'].append(
                {
                    'signal': signal,
                    'count': integer_segment[l],
                    'index': l % 18 + 1
                }
            )
        bp.data['blueprint']['entities'] += combinators

    return bp


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('image_path', type=str)
    imgpath = argparser.parse_args().image_path
    img = Image.open(imgpath)
    print(main(img).to_exchange_string())
