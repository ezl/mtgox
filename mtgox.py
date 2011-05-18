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
        return self._curl_mtgox(api=api)

    def get_recent_trades(self):
        api = "data/getTrades.php"
        return self._curl_mtgox(api=api)

# Authentication required methods
    def authenticate(self, username, password):
        self.username = username
        self.password = password

    def authentication_required(function):
        def wrapped(self, *args, **kwargs):
            if not (self.username and self.password):
                msg = "You must be authenticated to use this method"
                raise Exception, msg
            else:
                credentials = dict(username=self.username,
                                   password=self.password)
                return function(self, postdict=credentials, *args, **kwargs)
        return wrapped

    @authentication_required
    def get_funds(self, postdict):
        """Get your current balance.

           https://mtgox.com/code/getFunds.php?name=blah&pass=blah"""
        api = "getFunds.php"
        return self._curl_mtgox(api=api, postdict=postdict)

    @authentication_required
    def buy(self, quantity, price, postdict):
        """Place a buy order.
           Returns list of your open orders"""
        api = "buyBTC.php"
        return self._curl_mtgox(api=api, postdict=postdict)

    @authentication_required
    def sell(self, quantity, price, postdict):
        """Place a sell order.
           Returns list of your open orders"""
        api = "sellBTC.php"
        return self._curl_mtgox(api=api, postdict=postdict)

    @authentication_required
    def get_open_orders(self, postdict):
        """
        Returns:
            oid:    Order ID
            type:   1 for sell order or 2 for buy order
            status: 1 for active, 2 for not enough funds"""
        api = "getOrders.php"
        return self._curl_mtgox(api=api, postdict=postdict)

    @authentication_required
    def cancel(self, oid, order_type, postdict):
        """
           oid: Order ID
           type: 1 for sell order or 2 for buy order"""
        api = "cancelOrder.php"
        return self._curl_mtgox(api=api, postdict=postdict)

    @authentication_required
    def send(self, btca, amount, postdict, group1="BTC"):
        """Not really sure what this does or what the 'group1' arg is for, just copying from the API.

           https://mtgox.com/code/withdraw.php?name=blah&pass=blah&group1=BTC&btca=bitcoin_address_to_send_to&amount=#"""
        api = "withdraw.php"
        return self._curl_mtgox(api=api, postdict=postdict)

    def _curl_mtgox(self, api, postdict=None, timeout=8):
        BASE_URL = "http://mtgox.com/code/"
        url = BASE_URL + api
        if postdict:
            print postdict
            postdata = urllib.urlencode(postdict)
            print postdata
            request = urllib2.Request(url, postdata)
        else:
            request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=timeout)
        return response.read()

