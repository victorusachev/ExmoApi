from exmoapi.core.api import CoreApi


class PublicApi(CoreApi):
    def __init__(self,
                 api_url='https://api.exmo.com',
                 api_version='v1',
                 headers=(),
                 proxies=(),
                 connection_attempts=5):
        super().__init__(api_key=None, api_secret=None,
                         api_url=api_url, api_version=api_version,
                         headers=headers, proxies=proxies,
                         connection_attempts=connection_attempts)

    def trades(self, pairs):
        """
        List of the deals on currency pairs.

        Fields description:
            trade_id - deal identifier
            type - type of the deal
            price - deal price
            quantity - currency quantity
            amount - total sum of the deal
            date - date and time of the deal Unix

        :param pairs: one or various currency pairs separated by commas (example: BTC_USD,BTC_EUR)
        :return: dict
        """
        if isinstance(pairs, (list, tuple, set)):
            pairs = ','.join(pairs)
        if not isinstance(pairs, str):
            raise ValueError('The `pairs` argument must be a list, tuple, set or a string.')
        pairs = pairs.upper()

        trades = self.query('trades', params={'pair': pairs})
        return trades

    def order_book(self, pairs, limit=100):
        """
        The book of current orders on the currency pair.

        Fields description:
            ask_quantity - the sum of all quantity values in sell orders
            ask_amount - the sum of all total sum values in sell orders
            ask_top - minimum sell price
            bid_quantity - the sum of all quantity values in buy orders
            bid_amount - the sum of all total sum values in buy orders
            bid_top - maximum buy price
            bid - the list of buy orders where every field is: price, quantity and amount
            ask - the list of sell orders where every field is: price, quantity and amount

        :param limit: the number of displayed positions (default: 100, max: 1000)
        :param pairs: one or various currency pairs separated by commas (example: BTC_USD,BTC_EUR)
        :return: dict
        """
        if isinstance(pairs, (list, tuple, set)):
            pairs = ','.join(pairs)
        if not isinstance(pairs, str):
            raise ValueError('The `pairs` argument must be a list, tuple, set or a string.')
        pairs = pairs.upper()

        max_positions = 1000
        limit = min(limit, max_positions)
        response = self.query('order_book', params={'pair': pairs, 'limit': limit})
        return response

    def ticker(self):
        """
        Statistics on prices and volume of trades by currency pairs.

        Fields description:
            high - maximum deal price within the last 24 hours
            low - minimum deal price within the last 24 hours
            avg - average deal price within the last 24 hours
            vol - the volume of deals within the last 24 hours
            vol_curr - the total value of all deals within the last 24 hours
            last_trade - last deal price
            buy_price - current maximum buy price
            sell_price - current minimum sell price
            updated - date and time of data update
        :return: dict
        """
        response = self.query('ticker')
        return response

    def pair_settings(self):
        """
        Currency pairs settings.

        Fields description:
            min_quantity - minimum quantity for the order
            max_quantity - maximum quantity for the order
            min_price - minimum price for the order
            max_price - maximum price for the order
            min_amount - minimum total sum for the order
            max_amount - maximum total sum for the order
        :return: dict
        """
        response = self.query('pair_settings')
        return response

    def currency(self):
        """
        Currencies list.

        :return: list
        """
        response = self.query('currency')
        return response
