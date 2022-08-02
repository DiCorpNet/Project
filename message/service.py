import hashlib
from datetime import datetime


def hashsum_dialog():
    secret = datetime.now().strftime('%Y%m%d%H%M%S%f')
    secret_key = hashlib.sha1(str(secret).encode('utf-8')).hexdigest()
    # secret_key2 = hashlib.md5(str(secret).encode('utf-8')).hexdigest()
    return secret_key