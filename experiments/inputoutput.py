import codecs
import json
import os
from random import seed, shuffle
from nltk import word_tokenize



class IO:
    def __init__(self):
        self.trainpath = '../data/cleantext/'
        self.trainfile = '../data/train/field.csv'
        self.groundtruthpath = '../data/groundtruth/'

        urls, fids = self._getexamples()
        examples = zip(urls, fids)
        #examples = examples[70:100]
        print len(examples)

        # split into 3 sets :-3 fold CV
        self.set1, self.set2, self.set3 = self.split(examples)
        self.keys = ['Title', 'Body', 'Publish_date', 'Authors']
        return

    def split(self, examples):
        seed(3)
        shuffle(examples)
        return examples[:len(examples)/3], examples[len(examples)/3:-len(examples)/3], examples[-len(examples)/3:]

    def checkfornull(self, classifier_details):
        classifier, _ = classifier_details
        cnt = 0.0 
        totcnt = 0.0
        totcnt = 120
        temp = 120
        for testset in [self.set1, self.set2, self.set3]:
            urls, goldfid = zip(*testset)
            if temp > 0:
                urls = urls[temp:]
                goldfid = goldfid[temp:]
                temp -= len(testset)
            temp = max([temp, 0])

            for each in urls:
                p = classifier.predict(each)
                print 'Seeing %s ---- Title %s' % (each[:-30], p['Title'])
                totcnt += 1

                if p['Title'] is None or p['Title'].encode('UTF-8') == '':
                    print 'GOTIT %s' % (each)
                    cnt += 1
        return cnt / totcnt

    def _comparetitle(self, gold, pred):
        # consider tokenize and fscore.
        pred,gold = pred.lower(),gold.lower()
        print word_tokenize(pred), word_tokenize(gold), word_tokenize(gold) ==  word_tokenize(pred)
        return 1 if word_tokenize(gold) == word_tokenize(pred) else 0
        # pred = filter(lambda x: x !='', pred.lower().strip().split(' '))
        # gold = filter(lambda x: x !='', gold.lower().strip().split(' '))
        # print pred,gold, pred==gold
        
        # cmp = True
        # for x,y in zip(word_tokenize(pred),word_tokenize(gold)):
        #     print x,y, x==y.decode('utf-8')
        #     cmp = cmp and x==y.decode('utf-8')
        # print word_tokenize(pred),word_tokenize(gold), cmp
        # return cmp
        # pred = filter(lambda x: x !='', word_tokenize(pred))
        # gold = filter(lambda x: x !='', word_tokenize(gold))
        #return 1 if gold == pred else 0

    def _comparebody(self, pred, gold):
        # for now just get some number
        correct = 0
        tot = 10000

        for x, y in zip(pred.strip().split(), gold.strip().split()):
            if x == y:
                correct += 1
            tot += 1
        return correct / tot

    # fit a URL using fit
    # train on a set using train
    def evaluate(self, classifier_details):
        (classifier, foldername) = classifier_details
        res = []
        compare = []

        for testset in [self.set1, self.set2, self.set3]:
            # classifier.train()
            urls, goldfid = zip(*testset)
            acc = 0.0
            for url, fid in zip(urls, goldfid):
                fnametruth = self.groundtruthpath + 'Title/' + fid + '.groundtruth'
                #fp = open(fnametruth)
                
                fp = codecs.open(fnametruth, "r", "utf-8")
                groundtruth_title = fp.readlines()
                groundtruth_title = ' '.join(groundtruth_title)
                p = classifier.predict(url)
                compare.append((groundtruth_title, p['Title'].encode('UTF-8')))
                acc += self._comparetitle(groundtruth_title, p['Title'])
                self.writeprediction(p, fid, foldername)
            acc /= len(urls)
            res.append(acc)
        # print 'Results'
        # for x, y in compare:
        #   print x
        #   print y
        #   print self._comparetitle(x, y)
        #   print '-'*75
        return res, sum(res) / len(res), len(self.set1) + len(self.set2) + len(self.set3)

    def getexamples(self):
        urls = []
        fid = []
        td = open(self.trainfile)
        for each in td.readlines():
            k = each.strip().split(', ')
            fid.append(k[0])
            urls.append(k[1])
        return urls, fid

    def _getexamples(self):
        fids_dict = {}
        for each in os.listdir(self.groundtruthpath +'/Title'):
            res = ''
            for every in each:
                if every == '.':
                    break
                res += every
            fids_dict[res] = 1

        
        urls = []
        fid = []

        td = open(self.trainfile)
        for each in td.readlines():
            k = each.strip().split(',')
            if k[0] in fids_dict:
                # print k[0]
                urls.append(k[1])
                fid.append(k[0])
                fids_dict[k[0]] = k[1]
        
        return urls, fid

    # Need not be used
    def writeprediction(self, result, fid, foldername):
        fname = self.trainpath + foldername + '/' + fid + '.cleantext'
        with open(fname, 'w') as fp:
            json.dump(result, fp, ensure_ascii=False)
        return


#########################Testing#############################

class Temp:
    def predict(self, url):
        g = {}
        g['Body'] = ''
        g['Title'] = ''
        g['Publish_date'] = ''
        g['Authors'] = ''
        return g


if __name__ == '__main__':
    io = IO()
    t = Temp()
    io.checkfornull((t, None))
    #io.Evaluate((t, 'test'));
