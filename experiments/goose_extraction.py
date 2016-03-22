import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from goose import Goose

class GOOSE:
    def __init__(self,name=''):
        self.pygoose = Goose()
        return;

    def predict(self,url):
        print 'Predicting %s' %url
        #url = "http://hobbes.cs.umass.edu/~ranga/scrap/g12516.html"
        article = self.pygoose.extract(url=url)
        d = {}
        d['Body'] = article.cleaned_text
        d['Title'] = article.title      
        return d

    def train(self):
        return ;

if __name__ == '__main__':  
    from inputoutput import IO
    IO = IO()
    goose = GOOSE()
    #accuracies = IO.checkfornull((goose,'goose'))
    accuracies = IO.evaluate((goose,'goose'))
    print accuracies





