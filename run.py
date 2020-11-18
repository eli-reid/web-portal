"""
This script runs the Condo_Co_Op_Web application using a development server.
"""
import sys
from os import environ

from Condo_Admin import create_app
if  len(sys.argv) > 1:
    app = create_app(sys.argv[1])
else :
    app = create_app()
if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 5555
    try:
        app.run(HOST, PORT)
    except OSError:
        app.run(HOST, 5500)

