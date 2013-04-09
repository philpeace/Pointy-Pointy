import SessionManager
from google.appengine.api import memcache
import datetime
import random
import logging

class SessionManager(object):
    def __init__(self, request, response, timeout=1200):
        self.timeout = timeout
        self.request = request
        self.response = response
        self.cookieName = 'SID'

    def current(self):
        cookievalue = self.request.cookies.get(self.cookieName)

        if ((cookievalue is not None) and (memcache.get(cookievalue) is not None)):
            return Session(cookievalue, self.timeout, False)
            #logging.debug('SessionManager:Existing = ' + cookievalue)
        else: 
            #logging.debug('SessionManager:New')
            return self._createSession()

    def _createSession(self):
        newId = self.createNewId()
        memcache.set(key=newId, value=True, time=self.timeout,)

        now = datetime.datetime.now()
        inc = datetime.timedelta(seconds=self.timeout)
        now += inc
        self._setCookie(key=self.cookieName, value=newId, expires=now)
        #logging.debug('SessionManager:newId = ' + newId)
        
        return Session(newId, self.timeout, True)
        
    def destroySession(self):
        for key in self.current().keys():
            memcache.delete(key=key)
        
        self._clearCookie(self.cookieName)

    def createNewId(self):
        newHash = str(hash(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'))) + str(random.random())

        while memcache.get(newHash) is not None:
            newHash = self.CreateNewId()

        return newHash

    def _setCookie(self, key, value, expires, path='/'):
        self.response.headers.add_header('Set-Cookie', key + '=' + value + ' path=' + path + '; expires ' + expires.strftime('%a, %d-%b-%Y %H:%M:00 %Z'))

    def _clearCookie(self, key):
        self._setCookie(key=key, value='', expires=datetime.datetime.now())


class Session(object):
    def __init__(self, id, timeout, isNew=False):
        self.id = id
        self.timeout = timeout
        self.isNew = isNew
        self._keysKey = 'SID-' + self.id
        
        if self.isNew:
            #logging.debug('New Session')
            self.items = dict([('id', self.id)])
        else:
            #logging.debug('Existing Session')
            self.items = memcache.get(key=self._keysKey)
            #logging.debug('Session = ' + str(self.items))

        self._update()

    def get(self, key):
        return self.__getitem__(key=key)

    def set(self, key, value):
        return self.__setitem__(key=key, value=value)

    def __getitem__(self, key):
        if self.hasKey(key=key):
            val = self.items[key]
            #logging.debug('session.get(' + key + ') = ' + str(val))
            return val
        else:
            logging.debug('session.get(' + key + ') = None')
            return None

    def __setitem__(self, key, value):
        self.items[key] = value
        #logging.debug('session.set(' + key + ', ' + str(value) + ')')
        self._update()
        return value

    def hasKey(self, key):
        hk = (key in self.items.keys())
        #logging.debug('session.hasKey(' + key + ') = ' + str(hk))
        return hk

    def keys(self):
        return self.items.keys()

    def _update(self):
        memcache.set(key=self._keysKey, value=self.items, time=self.timeout)
