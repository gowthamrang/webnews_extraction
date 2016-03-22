import sys

from boilerpipe.extract import Extractor


reload(sys)
sys.setdefaultencoding('utf-8')


class BoilerPipe:
    def __init__(self, name=''):
        return

    def predict(self, url):
        print 'Predicting %s' %url
        try:
            article = Extractor(url=url)
        except:
            print 'Exception %s' %url
            d = {}
            d['Body'] = ''
            d['Title'] = ''
            # print d
            return d

        d = {}
        d['Body'] = ''
        d['Title'] = article.getTitle()
        if d['Title'] is None:
            d['Title'] = ''
        return d

    def train(self):
        return

if __name__ == '__main__':
    from inputoutput import IO
    io = IO()
    bp = BoilerPipe()
    # accuracies = io.checkfornull((bp, 'bp'))
    accuracies = io.evaluate((bp, 'boilerpipe'))
    print accuracies





