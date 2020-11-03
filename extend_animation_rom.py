import blueprint
from copy import deepcopy


bp = blueprint.Blueprint.from_exchange_string('0eNrtld1qwzAMhd9F1+lofrsZ+iRjhCRWW0FjB1suCyXvPiUZpWvHaK7Xm4AUnaOTD+OcoT4G7BwZBnUGaqzxoN7P4GlvquPY475DUECMLURgqnasNDak0a0a29ZkKrYOhgjIaPwEFQ8fEaBhYsLZbSr60oS2RicDf/lE0FkvUmvG7WK3ytP0JY+gB5UXuayRkOzssazxUJ1IJDL3bVTKOz2J/djdkfNc3n3LiRwH6VxizBMrbRlmf8/VSGQ9Fm1XuSmZgq1IbOAuLDDFE7qeD2T2s3fXS8hguNw525ZkxAwUu4DDvNpgc8kfj4+9QzTXGEmDSmWWXBOIp1KQD6K/I50sJZ38Z9IO9S3n7DHO6VLO8fNE35COHyOdLSW9fp7oH5yT3zjLhT1d8OrqfxCBbPcTy+Q1zjbZ26bYxOsiL4bhC3OAKfg=')
original = bp.data['blueprint']['entities']
bp.data['blueprint']['entities'] = []


def extend(n):
    for i in range(0, n):
        segment = deepcopy(original)
        for entity in segment:
            entity['position']['x'] += i * 5
            entity['entity_number'] += i * 4
            entity['control_behavior']['decider_conditions']['constant'] += i
            for connid, connection in entity['connections'].items():
                for color, data in connection.items():
                    for j, c in enumerate(data):
                        entity['connections'][connid][color][j]['entity_id'] = c['entity_id'] + i * 4
        bp.data['blueprint']['entities'] += segment


extend(300)
print(bp.to_exchange_string())
