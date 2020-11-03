import blueprint
from copy import deepcopy

EXCHANGE_STRING = '0eNrFnG9P2zAQh7+LX4fJf+4cp9I+yYRQgWyL1KZVmqIh1O++BMTGHE6zfdXlzUSztokfX53nfsW8qPvduT0OXT+qzYvqHg79SW2+vahT96Pf7uZj4/OxVRvVje1eVarf7udHp/P9adyO3aFXl0p1/WP7S23Mpfr/C/fb3e5mt90fP7zQXm4r1fZjN3bt2+lfHzzf9ef9fTtM7/zZ6yt1PJy612uYzja9zY01xn/BSj1PP9fTT9MZpgGNw2F3d9/+3D51h2F+6kM3PJy78W76v8c/r//eDafxbnH1T90wnqcjfy/g9Rk3j4dRvb39xGGGB2F+tD9uh+04n0Z9VZe3J/Ttw3yS0/yuZv7nx9C2/cdhdo8zg+qfx6a53F4uHw6+s7DJLGA1Fg2PhYlYOAKFS0Zh10KB+rplAQQKSEahV0NheChchAIJFPjZKvUZCt28g8i5DIguw8cfXGqKfOoU6Xq1KbK8KcKIRU2gqJNR4GooHA9FXBaBQBGSUbjVUAAPRR1/QjTBoklmsd4i5pm3tvjeZj0Bw+hkGmY1GsijEWIY1IJhUg1QN2E1GDUPRhN/TCwFwybDWE2HMVz5c2IoCTQumcZqQoxcIbapkmEg0X5040rsB5fTEh2gtMxg8jyttp55pq2bWA4Nubqn2qAOzWo0mMJuFsVCLu91Mo3V3Ngz3dgsGgVKCU1IprGaHnumHptYCh25ojUF4Q/K0nD2uoGHpQzZ6oL0RxoGtzRiEbKGomEKAiBpGszmaSqFiAalhdYWZEDSNJgNA10KriBdkR48s3e01BJpoSBPkR48szuysWhaSjQtFkQq0jQCuxQSO2frC0IVYRqgr9s5W8qsbF2QqUiXBrdX1MkflFAQqkiXBrMHsbF1W/J7taYgVZGmwfRMGwdujhJNpwtSFWkaTNEkS8GZgqhCevBMr3SURjpbkExID56pkW7xDTP5FbMrSCakaXh2KST24g4KkglpGkzRNCG5NjA/mfBalobh1kZ8/0SShs+PJsRpMGvDxYmmo7Tb1fnRhDiNcOXacJR3u5AfTYjTYHq3WySapF40ub+h4nXWlcQrGMQtAVATBTo/RpGeKMvsFl3cLgIVKoHJz1XEaTAbpGVtUGIINj9XEafBbJAgFkOgbnfg8qMEcRrMBgliMfRUuwiQnzKJ02B2TBDf/D25bmB+sCJOg9lCQZxAAvVVN/j8YEWchr9ybQAlhlDnByviNJiaDD7ZN0Lur6tkqlCznJfoAGVp0OSHQOITxTR4iE0RqQUedX4qJE6DafAQFwtSCzya/FRImoZjajLGYoiUGKLNT4XEaTA1GWMx9NSShi4/FcJGloa+cgyCVGCIkB8KScPgVsZiXwq5MQXzMyFpGNwNILEVImWF6PMjIWkYzPaJLoQ6P2WRHjuzWUJyeQz5mYr02JmtEcaOiZRjYpMfqUjD8OxCSMwQfMGGF2kY3MbIpVaGN/mBijSMcOUEwVOC6W1+niINg9l7+IVfUsGjd/lxirhSMQXTL4JHclMt5Mcp4jSYhkmXQsGWGvHBM43SUwLpC3bQiA+eu4l4ETlTsaIv2EEjTgPYpZDYg/uCHTTiNLiWaT+vjdvq7U+ubD78aZdKPbXD6fXCbTBQQ1P72mg/dWeX32a4vMg='

bp = blueprint.Blueprint.from_exchange_string(EXCHANGE_STRING)
og_segment = bp.data['blueprint']['entities']
entity_count = 17 * 4
bp.data['blueprint']['entities'] = []


def extend_right(n=2):
	global bp
	for i in range(0, n):
		segment = deepcopy(og_segment)
		for entity in segment:
			entity['position']['x'] += i * 32
			entity['entity_number'] += i * entity_count
			for connid, connection in entity['connections'].items():
				for color, data in connection.items():
					for j, c in enumerate(data):
						entity['connections'][connid][color][j]['entity_id'] = c['entity_id'] + i * entity_count
			if entity['name'] == 'small-lamp':
				entity['control_behavior']['circuit_condition']['constant'] += i * 32
		bp.data['blueprint']['entities'] += segment


def extend_completely():
	for i in range(0, 16):
		segment = deepcopy(og_segment)
		for entity in segment:
			entity['position']['x'] += i % 4 * 32
			entity['position']['y'] -= i // 4 * 32
			entity['entity_number'] += i * entity_count
			for connid, connection in entity['connections'].items():
				for color, data in connection.items():
					for j, c in enumerate(data):
						entity['connections'][connid][color][j]['entity_id'] = c['entity_id'] + i * entity_count
			if entity['name'] == 'small-lamp':
				entity['control_behavior']['circuit_condition']['constant'] += i * 64
				entity['control_behavior']['use_colors'] = True
		bp.data['blueprint']['entities'] += segment


extend_completely()
print(bp.to_exchange_string())
