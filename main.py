import random
import time

import api
import config
from api import logger
from api import servers


@logger.catch
def start():
    main = api.Client101(_type='main')
    server = random.choice(servers)
    logger.info(f'[INFO] Connected to {server[0]}:{server[1]} server')
    main.connect(server)
    key2 = main.getSessionKey()
    main.verifySession(key2)
    main.auth(config.TOKEN)

    for _ in range(100):
        bot = api.Client101(_type='bot')
        bot.connect(server)
        key = bot.getSessionKey()
        bot.verifySession(key)
        token = ''
        while not token:
            try:
                token = bot.register()
            except:
                continue
        bot.auth(token)
        bot.sendFriendRequest()
        _id1 = ''
        while not _id1:
            _id1 = main.getMessagesUpdate()
        main.acceptFriendRequest(_id1)
        for bet in [100, 5000]:
            pwd = bot.createGame(bet)
            bot.inviteToGame()
            _id = ''
            while not _id:
                _id = main.getInvites()
            main.join(_id, pwd)
            bot.ready()
            main.ready()
            time.sleep(.5)
            if bet == 100:
                main.exit()
            else:
                bot.exit()
            time.sleep(.5)
            main.leave(_id)
            bot.leave(_id)
            time.sleep(.5)
        main.deleteFriend(_id1)
        time.sleep(.5)


start()
