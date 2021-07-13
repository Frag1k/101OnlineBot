import json

import requests
from faker import Faker

faker = Faker('RU_ru')


def get_random_name():
    return faker.first_name()


def toBytes(data):
    return data.encode()


def unMarshal(data):
    result = [{}]
    for i in data.strip().split('\n'):
        pos = i.find('{')
        command = i[:pos]
        try:
            message = json.loads(i[pos:])
        except:
            continue
        message['command'] = command
        result.append(message)

    return result[1:] if len(result) > 1 else result


def marshal(data):
    return data.pop('command') + json.dumps(data, separators=(',', ':')).replace('{}', '') + '\n'


def getServers():
    data = requests.get('http://static.rstgames.com/101/servers.json').json()
    return [(data['user'][server]['host'], data['user'][server]['port']) for server in data['user'] if server != 'u0']
