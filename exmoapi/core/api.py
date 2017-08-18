import hashlib
import hmac
import time
from enum import Enum

import requests
from requests.models import urlencode

from exmoapi.core.utils import recursive_transform


class Credential(object):
    def __init__(self, api_key, api_secret):
        self._key = api_key
        self._secret = api_secret

    @property
    def key(self):
        return self._key

    @property
    def secret(self):
        return self._secret


class CoreApi(object):
    MAX_CONNECTION_ATTEMPTS = 10
    CONNECTION_ATTEMPTS_PAUSE = 5

    def __init__(self,
                 api_key=None,
                 api_secret=None,
                 api_url='https://api.exmo.com',
                 api_version='v1',
                 headers=(),
                 proxies=(),
                 connection_attempts=5):
        self._API_KEY = api_key
        self._API_SECRET = bytes(api_secret or '', encoding='utf-8')
        self._API_URL = api_url
        self._API_VERSION = api_version
        self._headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self._headers.update(headers)
        self._proxies = proxies or {}
        self._connection_attempts = CoreApi.MAX_CONNECTION_ATTEMPTS
        self.connection_attempts = connection_attempts
        self._last_nonce = 0

    @property
    def connection_attempts(self):
        return self._connection_attempts

    @connection_attempts.setter
    def connection_attempts(self, value):
        """
        Sets the number of connection attempts.

        :param value: the number of attempts (default: 10, max: 10)
        :return:
        """
        if 0 < value <= CoreApi.MAX_CONNECTION_ATTEMPTS:
            self._connection_attempts = value
        else:
            self._connection_attempts = CoreApi.MAX_CONNECTION_ATTEMPTS

    def query(self, api_endpoint, params=None, http_method='post'):
        """
        Performs an request to API with the specified parameters.

        In the presence of api_key and api_secret query will contain a nonce and additional headers:
        - Key is a public API key,
        - Sign is a cryptographic signature based on a hash of all parameters and public key.

        :param api_endpoint: API endpoint
        :param params: query parameters
        :param http_method: request method (GET or POST).
        :return:
        """
        http_method = http_method.lower()
        if http_method not in ('get', 'post'):
            raise ValueError("Parameter `http_method` must be 'get' or 'post' (default: 'post').")

        url = f'{self._API_URL}/{self._API_VERSION}/{api_endpoint}'
        params = params or {}
        headers = dict(self._headers)

        response = None
        attempts = int(self._connection_attempts)
        while attempts:
            attempts -= 1
            try:
                if self._API_KEY and self._API_SECRET:
                    self._sign(headers, params)
                response = requests.request(http_method, url, data=params, headers=headers, proxies=self._proxies)
                break
            except Exception as e:
                if not attempts:
                    raise e
                print(e)
                print('Retrying in 5 seconds...')
                time.sleep(CoreApi.CONNECTION_ATTEMPTS_PAUSE)

        # The processing of the response is carried out in a separate try-except block
        # in order to exclude the repeated execution of the non-idempotent query.
        try:
            obj = response.json()
            if isinstance(obj, dict):
                err = obj.get('error')
                if err:
                    raise Exception(err)
            return recursive_transform(obj)
        except Exception as e:
            raise e

    def ping(self):
        """
        Checks the connection with the API server.

        Returns True if the connection is established, otherwise False.
        :return: True or False
        """
        api_endpoint = 'currency'
        url = f'{self._API_URL}/{self._API_VERSION}/{api_endpoint}'
        response = requests.get(url, proxies=self._proxies)
        return response.ok

    @property
    def next_nonce(self):
        """
        All the requests should include the obligatory POST parameter `nonce` with incremental numerical value (>0).
        The incremental numerical value should never reiterate or decrease.

        The parameter `nonce` is used to sign the request parameters in order to ensure security.
        :return: unique increasing integer
        """
        while True:
            nonce = int(round(time.time() * 1000))
            if nonce > self._last_nonce:
                self._last_nonce = nonce
                return nonce

    def _sign(self, headers, params):
        params['nonce'] = self.next_nonce
        headers.update({'Key': self._API_KEY})
        headers.update({'Sign': self._sha512(urlencode(params))})

    def _sha512(self, data):
        # hash-based message authentication code
        hash_obj = hmac.new(key=self._API_SECRET, digestmod=hashlib.sha512)
        hash_obj.update(data.encode('utf-8'))
        return hash_obj.hexdigest()

