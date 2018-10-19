import responder

from backend.oauth.app import oauth_app

api = responder.API()

api.mount('/flask', oauth_app)

if __name__ == '__main__':
    api.run(port=5000)
