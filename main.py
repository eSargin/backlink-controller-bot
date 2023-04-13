import json

import cache
import redisoperation
import service
import utils
from server import app
from jproperties import Properties

proxyList = []


def debug(param):
    key = redisoperation
    # redis get to string
    key = key.decode('utf-8')
    print(key)
    exit(1)


def LoadProgram():
    configs = Properties()

    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)

    items_view = configs.items()
    list_keys = []

    for item in items_view:
        list_keys.append(item[0])

    print(list_keys)
    # ['DB_HOST', 'DB_SCHEMA', 'DB_User', 'DB_PWD']


if __name__ == '__main__':

    # serviceResponse = service.startService(1)
    # JwtExample()
    # exit(1)
    proxyList = utils.loadProxyList()
    if proxyList is not None:
        jsonData = json.loads(proxyList)
        cache.proxyList = jsonData['data']
        print('Proxy List Size : ', len(cache.proxyList))
        # print(proxyList)
    else:
        print("Proxy List Load Error!")
    app.run(host="0.0.0.0", port=7000)
