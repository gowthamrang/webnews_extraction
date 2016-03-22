from newspaper import Article
from inputoutput3 import IO


class NewsPaper:
    def __init__(self, name=''):        
        return

    def predict(self, url):
        print('Predicting', url)
        try:
            article = Article(url)
            article.download()
            article.parse()
        except:
            print('Exception %s' %url)
            d = {}
            d['Body'] = ''
            d['Title'] = ''

            return d

        d = {}
        d['Body'] = ''
        d['Title'] = article.title

        if d['Title'] == None:
            d['Title'] = ''
        # print('Title',  d['Title'])
        return d

    def train(self):
        return

if __name__ == '__main__':
    io = IO()
    np = NewsPaper()
    print('Newspaper Evaluation')
    # accuracies = io.checkfornull((bp, 'bp'))
    accuracies = io.Evaluate((np, 'newspaper'))
    print(accuracies)




