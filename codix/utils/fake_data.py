import json

fake_data = {'history': [()], # [(date, observer, comment), ...]
      'media': '/home/zarpe/Documents/M2U01284.MPG', # path for the media file
      'code': {"date": "Thu Feb  9 18:22:37 2023", 
               "project": "Test", 
               "description": "", 
               "period": 5.0, 
               "codes": {"code_1": ["s1", "s2", "s3"]}, 
               "sites": {"Site_1": ["code_1"]}}, # dictionary from the code file
      'times': [0, 5000, 10000], # sample times (in ms)
      'comments': ['','',''], # sample comments
      'data': {'Site_1': {'code_1':{'alphabet': ['s1','s2','s3'], 'seq': [0,1,2]}}}} # data

with open('fdata.cdx', 'w') as ff:
    json.dump(fake_data, ff)
