import argparse
import blueprint
from PIL import Image, ImageSequence
from pathlib import Path
import convert_for_display


argparser = argparse.ArgumentParser()
argparser.add_argument('image_path', type=str)
seqpath = argparser.parse_args().image_path

image = Image.open(seqpath)
directory = Path('.') / 'animation_output'
for filename in directory.glob('*'):
    filename.unlink()
print(f'Frames: {image.n_frames}')
print(f'Framerate: {1000 / image.info["duration"]} ({image.info["duration"] / (1000 / 60)} ticks per frame)')
bp = blueprint.Blueprint.from_exchange_string('0eNptjsEKwjAQRP9lzhGspInNr4hIq4sstNvSbMVS8u828eLB28yw82Y3dP1C08yiCBv4PkpEuGyI/JS2z5muEyGAlQYYSDtkF5cuaqs8CpIBy4PeCFW6GpAoK9OXUsx6k2XoaN4P/vUNpjFykfvajjnU1hqsCLVrUkaW6fDzqcGL5lgap3NlvW2889XR1S6lD4zTRSo=')
bp.data['blueprint']['entities'] = []

for i, frame in zip(range(image.n_frames), ImageSequence.Iterator(image)):
    segment = convert_for_display.main(frame).data['blueprint']['entities']
    entity_count = len(segment)
    for e in segment:
        e['entity_number'] += i * entity_count
        e['position']['y'] += i * 5
    bp.data['blueprint']['entities'] += segment

with open('output/animation.txt', 'w') as f:
    f.write(bp.to_exchange_string())
