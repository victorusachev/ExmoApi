from exmoapi.public import PublicApi


class AuthenticatedApi(PublicApi):
    def __init__(self, api_key, api_secret, *args, **kwargs):
        if not (api_key and api_secret):
            raise ValueError('Parameters `api_key` and `api_secret` must be specified.')
        # kwargs.update({'api_key': api_key, 'api_secret': api_secret})
        super().__init__(api_key=api_key, api_secret=api_secret, *args, **kwargs)

    def user_info(self):
        """
        Getting information about user's account.

        Fields description:
            uid - user identifier
            server_date - server date and time
            balances - user's available balance
            reserved - user's balance in orders

        :return: dict
        """
        response = self.query('user_info')
        return response

    def order_create(self, pair, quantity, price, typ):
        """
        Order creation.

        Fields description:
            result - 'true' in case of successful creation and 'false' in case of an error
            error - contains the text of the error
            order_id - order identifier

        :param pair: currency pair
        :param quantity: quantity for the order
        :param price: price for the order
        :param typ: type of order (values: buy, sell, market_buy, market_sell, market_buy_total, market_sell_total)
        :return: dict
        """
        assert pair
        types = ('buy', 'sell', 'market_buy', 'market_sell', 'market_buy_total', 'market_sell_total')
        if typ not in types:
            raise ValueError(f'The order type `{typ}` is invalid. Possible types: {", ".join(types)}')
        response = self.query('order_create', params=dict(pair=pair, quantity=quantity, price=price, type=typ))
        return response

    def order_cancel(self, order_id):
        """
        Order cancellation.

        Fields description:
            result - 'true' in case of sucessful creation of task for order cancellation and 'false' in case of an error
            error - containd the error description

        :param order_id: order identifier
        :return: dict
        """
        response = self.query('order_cancel', params=dict(order_id=order_id))
        return response

    def user_open_orders(self):
        """
        Getting the list of user’s active orders.

        Fields description:
            order_id - order identifier
            created - date and time of order creation
            type - type of order
            pair - currency pair
            price - price in the order
            quantity – quantity in the order
            amount – sum of the order

        :return: dict
        """
        response = self.query('user_open_orders')
        return response

    def user_trades(self, pair, offset=0, limit=100):
        """
        Getting the list of user’s deals.

        Fields description:
            trade_id - deal identifier
            date – date and time of the deal
            type - type of the deal
            pair - currency pair
            order_id - user’s order identifier
            quantity - currency quantity
            price - deal price
            amount - total sum of the deal

        :param pair: one or various currency pairs separated by commas (example: BTC_USD,BTC_EUR)
        :param offset: last deal offset (default: 0)
        :param limit: the number of returned deals (default: 100, мmaximum: 10 000)
        :return: dict
        """
        response = self.query('user_trades', params=dict(pair=pair, offset=offset, limit=limit))
        return response

    def user_cancelled_orders(self, offset=0, limit=100):
        """
        Getting the list of user’s cancelled orders.

        Fields description:
            date - date and time of order cancellation
            order_id - order identifier
            order_type – type of order
            pair - currency pair
            price – price in the order
            quantity – quantity in the order
            amount – sum of the order

        :param offset: last deal offset (default: 0)
        :param limit: the number of returned deals (default: 100, мmaximum: 10 000)
        :return: dict
        """
        response = self.query('user_cancelled_orders', params=dict(offset=offset, limit=limit))
        return response

    def order_trades(self, order_id):
        """
        Getting the history of deals with the order.

        Fields description:
            type – type of order
            in_currency – incoming currency
            in_amount - amount of incoming currency
            out_currency - outcoming currency
            out_amount - amount of outcoming currency
            trades - deals dict where the values mean the following:
                trade_id - deal identifier
                date - date of the deal
                type - type of the deal
                pair - currency pair
                order_id - order identifier
                quantity - currency quantity
                price - deal price
                amount - sum of the deal

        :param order_id: order identifier
        :return: dict
        """
        response = self.query('order_trades', params=dict(order_id=order_id))
        return response

    def required_amount(self, pair, quantity):
        """
        Calculating the sum of buying a certain amount of currency for the particular currency pair.

        Fields description:
            quantity – quantity you can to buy
            amount - the sum you will spend
            avg_price - average buy price

        :param pair: currency pair
        :param quantity: quantity to buy
        :return: dict
        """
        response = self.query('required_amount', params=dict(pair=pair, quantity=quantity))
        return response

    def deposit_address(self):
        """
        Getting the list of addresses for cryptocurrency deposit.

        :return: dict
        """
        response = self.query('deposit_address')
        return response

    def withdraw_crypt(self, amount, currency, address):
        """
        Creation of the task for cryptocurrency withdrawal.

        Fields description:
            result - 'true' in case of successful creation of withdrawal task and 'false' in case of an error
            error - contains the error description
            task_id - withdrawal task identifier

        :param amount: amount of currency to be withdrawn
        :param currency: name of the currency to be withdrawn
        :param address: withdrawal adress
        :return: dict
        """
        response = self.query('withdraw_crypt', params=dict(amount=amount, currency=currency, address=address))
        return response

    def withdraw_get_txid(self, task_id):
        """
        Getting the transaction ID in order to keep track of it on blockchain.

        Fields description:
            result - 'true' in case of successful creation of withdrawal task and 'false' in case of an error
            error - contains the error description
            status - 'true' if the withdrawal is already done
            txid - transaction ID that should be used for tracking it on blockchain

        :param task_id: withdrawal task identifier
        :return: dict
        """
        response = self.query('withdraw_get_txid', params=dict(task_id=task_id))
        return response
