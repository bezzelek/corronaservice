from socket import gethostname, gethostbyname


bind = f'{gethostbyname(gethostname())}:5000'
workers = 2
threads = 4

loglevel = 'warning'
