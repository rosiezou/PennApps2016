import requests
import numpy
import threading
DB = requests.get('heroku db for stickers and their historic prices')
url = 'heroku endpoint'

def lstsqest(ticker):
  threading.Timer(10.0, getstd).start()
  m, c = numpy.linalg.lstsq(DB[ticker][price], DB[ticker][timestamp])
  requests.post(url, m*(time()-30)+c)

# updates the price chart