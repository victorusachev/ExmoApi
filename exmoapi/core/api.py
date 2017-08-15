import hashlib
import hmac
import time

import requests
from requests.models import urlencode


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
        self._API_URL = api_url
        self._API_VERSION = api_version
        self._API_KEY = api_key
        self._API_SECRET = bytes(api_secret or '', encoding='utf-8')
        self._proxies = proxies or {}
        self._headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self._headers.update(headers)
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

    def query(self, api_endpoint, params=None, request_method='post'):
        """
        Performs an request to API with the specified parameters.

        In the presence of api_key and api_secret query will contain a nonce and additional headers:
        - Key is a public API key,
        - Sign is a cryptographic signature based on a hash of all parameters and public key.

        :param api_endpoint: API endpoint
        :param params: query parameters
        :param request_method: request method (GET or POST).
        :return:
        """
        req_method = request_method.lower()
        if req_method not in ('get', 'post'):
            raise ValueError("The request method must be 'get' or 'post'")

        url = f'{self._API_URL}/{self._API_VERSION}/{api_endpoint}'
        params = params or {}
        headers = self._headers

        if self._API_KEY and self._API_SECRET:
            self._sign(headers, params)

        for _ in range(0, self._connection_attempts + 1):
            try:
                response = requests.request(req_method, url, data=params, headers=headers, proxies=self._proxies)
            except Exception as e:
                print(e)
                print('Retrying in 5 seconds...')
                time.sleep(CoreApi.CONNECTION_ATTEMPTS_PAUSE)
                continue

            # The processing of the response is carried out in a separate try-except block
            # in order to exclude the repeated execution of the non-idempotent query.
            try:
                obj = response.json()
                if isinstance(obj, dict):
                    err = obj.get('error')
                    if err:
                        raise Exception(err)

                def recursive_transform(obj):
                    """Recursive converting object to properly handle int and float."""
                    if isinstance(obj, dict):
                        rv = {}
                        for k, v in obj.items():
                            rv.update({k: recursive_transform(v)})
                        return rv
                    if isinstance(obj, (list, tuple, set, frozenset)):
                        rv = []
                        for el in obj:
                            rv.append(recursive_transform(el))
                        return type(obj)(rv)
                    if isinstance(obj, str):

                        if obj.isdecimal():
                            rv = int(obj)
                        else:
                            try:
                                rv = float(obj)
                            except:
                                rv = obj
                        return rv

                obj = recursive_transform(obj)

                return obj
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
                break
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

