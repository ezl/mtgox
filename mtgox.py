import urllib, urllib2
import json

# https://mtgox.com/support/tradeAPI

# urllib2.Request

class MtGox(object):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

# Public methods
    def ticker_data(self):
        """Get ticker data"""
        api = "data/ticker.php"
        return self._curl_mtgox(api=api)

    def market_depth(self):
        """Get market depth"""
        api = "data/getDepth.php"
        return self._curl_mtgox(api=api)

    def recent_trades(self):
        """Get recent trades"""
        api = "data/getTrades.php"
        return self._curl_mtgox(api=api)

# Authentication required methods
    def authenticate(self, username, password):
        """Set MtGox authentication information"""
        self.username = username
        self.password = password

    def authentication_required(function):
        def wrapped(self, *args, **kwargs):
            if not (self.username and self.password):
                msg = "You must be authenticated to use this method"
                raise Exception, msg
            else:
                credentials = {'name':self.username,
                               'pass':self.password}
                return function(self, postdict=credentials, *args, **kwargs)
        return wrapped

    @authentication_required
    def funds(self, postdict):
        """Get your current balance."""
        api = "getFunds.php"
        return self._curl_mtgox(api=api, postdict=postdict)

    @authentication_required
    def buy(self, amount, price, postdict):
        """Place a buy order.
           Returns list of your open orders"""
        api = "buyBTC.php"
        postdict.update(dict(amount=amount,
                             price=price))
        return self._curl_mtgox(api=api, postdict=postdict)

    @authentication_required
    def sell(self, amount, price, postdict):
        """Place a sell order.
           Returns list of your open orders"""
        api = "sellBTC.php"
        postdict.update(dict(amount=amount,
                             price=price))
        return self._curl_mtgox(api=api, postdict=postdict)

    @authentication_required
    def open_orders(self, postdict):
        """Get open orders.

        In response, these keys:
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
        BASE_URL = "https://mtgox.com/code/"
        url = BASE_URL + api
        if postdict:
            postdata = urllib.urlencode(postdict)
            request = urllib2.Request(url, postdata)
        else:
            request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=timeout)
        return response.read()

