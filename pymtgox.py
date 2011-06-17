import websocket # websocket-client==0.4.1, installable via pip
import cjson

def serialize(obj):
    return cjson.encode(obj)

def deserialize(msg):
    return cjson.decode(msg)

CHANNELS = {
    "dbf1dee9-4f2e-4a08-8cb7-748919a71b21": "trades",
    "d5f06780-30a8-4a48-a2f8-7ed181b4a13f": "ticker",
    "24e67e0d-1cad-4cc0-9e7a-f8523ef460fe": "depth",
}

def on_message(ws, message):
    data = deserialize(message)
    channel = CHANNELS.get(data.get('channel'))

    if channel == "trades":
        print "TRADE: %s" % data.get("trade")
    elif channel == "depth":
        print "DEPTH: %s" % data.get("depth")
    elif channel == "ticker":
        print "TICKER: %s" % data.get("ticker")
    else:
        pass

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### connected ###"

if __name__ == "__main__":
    websocket.enableTrace(False)
    url = 'ws://websocket.mtgox.com/mtgox'
    ws = websocket.WebSocketApp(url,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
