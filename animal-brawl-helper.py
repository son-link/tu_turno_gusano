from os import path, environ

LOCAL_DIR = path.dirname(path.realpath(__file__))
environ['SSL_CERT_FILE'] = path.join(LOCAL_DIR, 'certifi', 'cacert.pem')
from abh import run

run()
