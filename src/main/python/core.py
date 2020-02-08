fbs = None
_app = None

def setApp(__app):
    global _app
    _app = __app

def app():
    return _app