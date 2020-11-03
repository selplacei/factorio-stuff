import blueprint
from PIL import Image
from pathlib import Path
import convert_for_display
import sys


directory = Path('.') / 'animation_output'
for filename in directory.glob('*'):
    filename.unlink()
print(f'Frames: {len(sys.argv) - 1}')
bp = blueprint.Blueprint.from_exchange_string('0eNptjsEKwjAQRP9lzhGspInNr4hIq4sstNvSbMVS8u828eLB28yw82Y3dP1C08yiCBv4PkpEuGyI/JS2z5muEyGAlQYYSDtkF5cuaqs8CpIBy4PeCFW6GpAoK9OXUsx6k2XoaN4P/vUNpjFykfvajjnU1hqsCLVrUkaW6fDzqcGL5lgap3NlvW2889XR1S6lD4zTRSo=')
bp.data['blueprint']['entities'] = []

for i, frame in enumerate(sys.argv[1:]):
    segment = convert_for_display.main(Image.open(frame)).data['blueprint']['entities']
    entity_count = len(segment)
    for e in segment:
        e['entity_number'] += i * entity_count
        e['position']['y'] += i * 5
    bp.data['blueprint']['entities'] += segment

with open('output/animation.txt', 'w') as f:
    f.write(bp.to_exchange_string())
