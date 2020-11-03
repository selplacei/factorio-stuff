# Change the number on the last line in this file to suit your needs. It is the amount of 4-KiB segments,
# and can *theoretically* go up to 4194304.
# When you run this, there will be several files named "multiply_X.txt". Each one is an exchange string to be pasted
# into the world. You'll have to connect the wires between each segment manually, but you can do that by just
# copy-pasting pairs of substations that have a green wire connection between them on top of the segments.
# The reason why these are split is because my computer can't handle a single blueprint the size of four 4-KiB cells.
# If you want a try at it, uncomment all commented lines and replace the
# "new_bp" part with "bp.data['blueprint']['entities'] += segment".
import blueprint
import math
from copy import deepcopy


bp = None
with open('data/memcell.txt') as f:
	bp = blueprint.Blueprint.from_exchange_string(f.read().strip())

original = deepcopy(bp.data['blueprint']['entities'])
bp.data['blueprint']['entities'] = []


def multiply(n):
	if math.sqrt(n) % 1 > 0:
		print('Warning: n is not a square')
	width = int(math.sqrt(n))
	entity_count = len(original)
	for i in range(0, n):
		segment = deepcopy(original)
		x_offset = i % width * OG_WIDTH
		y_offset = -(i // width * OG_HEIGHT)
		for entity in segment:
			entity['position']['x'] += x_offset
			entity['position']['x'] += y_offset
			entity['entity_number'] += entity_count * i
			if (
				entity['name'] == 'decider-combinator'
				and entity['control_behavior']['decider_conditions']['first_signal']['name'] != 'signal-red'
				and not (
					entity['control_behavior']['decider_conditions']['first_signal']['name'] == 'signal-info'
					and entity['control_behavior']['decider_conditions']['copy_count_from_input']
				)
			):
				entity['control_behavior']['decider_conditions']['constant'] += OG_MEM_WORDS * i
			elif entity['name'] == 'small-lamp':
				entity['control_behavior']['circuit_condition']['constant'] += OG_MEM_WORDS * i
			for connid, connection in entity['connections'].items():
				for color, data in connection.items():
					for j, c in enumerate(data):
						entity['connections'][connid][color][j]['entity_id'] = c['entity_id'] + i * entity_count
			bp.data['blueprint']['entities'] += segment
	with open('output/multiply.txt', 'w') as f:
		f.write(bp.to_exchange_string())


def multiply_and_segment(n):
	if math.sqrt(n) % 1 > 0:
		print('Warning: n is not a square')
	# width = int(math.sqrt(n))
	# entity_count = len(original)
	for i in range(0, n):
		segment = deepcopy(original)
		# x_offset = i % width * OG_WIDTH
		# y_offset = -(i // width * OG_HEIGHT)
		for entity in segment:
			# entity['position']['x'] += x_offset
			# entity['position']['x'] += y_offset
			# entity['entity_number'] += entity_count * i
			if (
				entity['name'] == 'decider-combinator'
				and entity['control_behavior']['decider_conditions']['first_signal']['name'] != 'signal-red'
				and not (
					entity['control_behavior']['decider_conditions']['first_signal']['name'] == 'signal-info'
					and entity['control_behavior']['decider_conditions']['copy_count_from_input']
				)
			):
				entity['control_behavior']['decider_conditions']['constant'] += OG_MEM_WORDS * i
			elif entity['name'] == 'small-lamp':
				entity['control_behavior']['circuit_condition']['constant'] += OG_MEM_WORDS * i
			# for connid, connection in entity['connections'].items():
			# 	for color, data in connection.items():
			# 		for j, c in enumerate(data):
			# 			entity['connections'][connid][color][j]['entity_id'] = c['entity_id'] + i * entity_count
		new_bp = blueprint.Blueprint(deepcopy(bp.data), bp.version_byte)
		new_bp.data['blueprint']['entities'] = segment
		with open(f'output/multiply_{i}.txt', 'w') as f:
			f.write(new_bp.to_exchange_string())
		del new_bp


OG_WIDTH = 128
OG_HEIGHT = 128
OG_MEM_WORDS = 1024

multiply_and_segment(4)
