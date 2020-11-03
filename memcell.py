import blueprint
from exchange_string import EXCHANGE_STRING
import sys
import json
from copy import deepcopy

# bp = blueprint.Blueprint.from_exchange_string(sys.stdin.read().strip())
bp = blueprint.Blueprint.from_exchange_string(EXCHANGE_STRING)
# print(json.dumps(bp.data, indent=4))

og_segment = sorted(
    bp.data['blueprint']['entities'],
    key=lambda ent: -10000 * ent['position']['y'] + ent['position']['x']
)
entity_number = 7 * 16 * 4 + 4
bp.data['blueprint']['entities'] = []

for i in range(0, 16):
    segment = deepcopy(og_segment)
    for entity in segment:
        entity['position']['x'] += i % 4 * 32
        entity['position']['y'] -= i // 4 * 32
        entity['entity_number'] += i * entity_number
        if (
            entity['name'] == 'decider-combinator'
            and entity['control_behavior']['decider_conditions']['first_signal']['name'] != 'signal-red'
            and not (
                entity['control_behavior']['decider_conditions']['first_signal']['name'] == 'signal-info'
                and entity['control_behavior']['decider_conditions']['copy_count_from_input']
            )
        ):
            entity['control_behavior']['decider_conditions']['constant'] += 64 * i
        for connid, connection in entity['connections'].items():
            for color, data in connection.items():
                for j, c in enumerate(data):
                    entity['connections'][connid][color][j]['entity_id'] = c['entity_id'] + i * entity_number
    bp.data['blueprint']['entities'] += segment

# for i in range(0, 64):
#     segment = deepcopy(og_segment)
#     for entity in segment:
#         if entity['entity_number'] in {1, 2, 5}:
#             entity['control_behavior']['decider_conditions']['constant'] += i
#         entity['entity_number'] += i * 7
#         entity['position']['x'] += i % 16 * 2
#         entity['position']['y'] -= i // 16 * 8
#         for connid, connection in entity['connections'].items():
#             for color, data in connection.items():
#                 for j, c in enumerate(data):
#                     entity['connections'][connid][color][j]['entity_id'] = c['entity_id'] + i * 7
#     bp.data['blueprint']['entities'] += segment


# print(json.dumps(bp.data, indent=4))
print(bp.to_exchange_string())
