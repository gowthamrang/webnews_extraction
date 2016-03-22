
import urllib
from readability.readability import Document
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Readablility:
    def predict(self, url):
        print 'Predicting %s' %url
        d = {}
        d['Body'] = ''
        d['Title'] = ''
        try:
            html = urllib.urlopen(url).read()
            d['Body'] = Document(html).summary()
            d['Title'] = Document(html).short_title()
        except:
            print 'Exception %s' %url
            return d
        if d['Title'] is None:
            d['Title'] = ''

        return d

if __name__ == '__main__':
    from inputoutput import IO
    io = IO()
    rb = Readablility()
    accuracies = io.evaluate((rb, 'readability'))
    print accuracies
