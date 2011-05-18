import urllib, urllib2
import json

# https://mtgox.com/support/tradeAPI

# urllib2.Request

class MtGox(object):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    # Public methods
    def get_ticker_data(self):
        api = "data/ticker.php"
        return self._curl_mtgox(api=api)

    def get_market_depth(self):
        api = "data/getDepth.php"

    def get_recent_trades(self):
        api = "data/getTrades.php"

    # Authentication required methods
    def authenticate(self):
        pass

    @staticmethod
    def authentication_required(function=None):
        if not self.username or not self.password:
            msg = "You must be authenticated to use this method"
            raise Exception, msg
        return function


    def get_funds(self):
        """Get your current balance."""
        pass

    def buy(self, quantity, price):
        """Place a buy order.
           Returns list of your open orders"""
        pass

    def sell(self, quantity, price):
        """Place a sell order.
           Returns list of your open orders"""
        pass

    def get_open_orders(self):
        """
        Returns:
            oid:    Order ID
            type:   1 for sell order or 2 for buy order
            status: 1 for active, 2 for not enough funds"""
        pass

    def cancel(self, oid, order_type):
        """
           oid: Order ID
           type: 1 for sell order or 2 for buy order
        """
        pass

    def send(self, group1="BTC", btca=None, amount=None):
        """Not really sure what this does or what the 'group1' arg is for, just copying from the API.

           https://mtgox.com/code/withdraw.php?name=blah&pass=blah&group1=BTC&btca=bitcoin_address_to_send_to&amount=#"""
        pass

    def _curl_mtgox(self, api, postdict=None, timeout=8):
        BASE_URL = "http://mtgox.com/code/"
        url = BASE_URL + api
        if postdict:
            request = urllib2.Request(url, data)
        else:
            request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=timeout)
        return response.read()

