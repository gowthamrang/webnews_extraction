import json
import os
from random import shuffle, seed
from nltk import word_tokenize

class IO:
    def __init__(self):
        # read from file
        # split into 3 sets :-3 fold CV
        # pass a classifier
        self.trainpath = '../data/cleantext/'
        self.trainfile = '../data/train/field.csv'
        self.groundtruthpath = '../data/groundtruth/'

        urls, fids = self._getExamples()
        examples = []
        for each in zip(urls, fids):
            examples.append(each)
        #examples = examples[30:45]
        print(len(examples))
        self.set1, self.set2, self.set3 = self.split(examples)
        self.keys = ['Title','Body','Publish_date','Authors']

    def split(self, examples):
        seed(3)
        shuffle(examples)
        l = int(len(examples)/3)
        return examples[:l], examples[l:-l], examples[-l:]


    def checkfornull(self, classifier_details):
        classifier, _ = classifier_details
        cnt = 0.0 
        totcnt = 0.0
        totcnt = 120
        temp = 120
        for testset in [self.set1, self.set2, self.set3]:

            urls, goldfid = zip(*testset)

            if temp>0:
                urls = urls[temp:]
                goldfid = goldfid[temp:]
                temp-=len(testset)
            temp = max([temp, 0])

            for each in urls:
                p = classifier.predict(each)
                print('Seeing %s ---- Title %s' % (each[:-30], p['Title']))
                totcnt+=1

                if p['Title'] is None or p['Title'].encode('UTF-8') == '':
                    print('GOTIT %s' % (each))
                    cnt+=1
        return cnt/totcnt


    def _compareTitle(self, gold, pred):
        return 1 if word_tokenize(gold) == word_tokenize(pred) else 0
        # pred1 = filter( lambda x: x!='', pred.lower().strip().split(' '))
        # gold1 = filter( lambda x: x!='', gold.lower().strip().split(' '))
        # print(pred.lower().strip().split())
        # print(gold.lower().strip().split())
        # i,j = 0,0
        # while i<len(pred) and j<len(gold):
        #     if pred[i] == '':
        #         i+=1
        #     elif gold[j] == '':
        #         j+=1
        #     elif gold[j]!=pred[i]:
        #         return 0
        #     i+=1
        #     j+=1

        # for x, y in zip(pred1, gold1):
        #     print(x,y)
        #     if x!=y:
        #         print('FAIL', x,y)
        #         return 0
        s = 0
        for each in gold1: s+=1
        for each in pred1: s-=1
        return 1 if s == 0 else 0

    def _compareBody(self, pred, gold):
        correct = 0
        tot = 10000

        for x, y in zip(pred.strip().split(), gold.strip().split()):
            if x==y:
                correct+=1
            tot+=1
        return correct/tot;
    # fit a URL using fit
    # train on a set using train
    def Evaluate(self, classifier_details):
        # classifier.    
        # classifier.train()
        (classifier, foldername) = classifier_details
        res = []
        compare = []
        for testset in [self.set1, self.set2, self.set3]:
            #TRAIN HERE
            urls, goldfid = zip(*testset)
            # urls, goldfid = zip(*self.set1)
            # pred = classifier.predict(urls)
            acc = 0.0
            #Compare body
            for url, fid in zip(urls, goldfid):
                #fname = self.trainpath+'groundtruth/'+fid+'.groundtruth.cleantext'
                fnametruth = self.groundtruthpath +'Title/'+fid+'.groundtruth'
                fp = open(fnametruth)
                groundtruth_title = fp.readlines()
                groundtruth_title = ' '.join(groundtruth_title)
                p = classifier.predict(url)
                #print 'Comparing predicted %s with Gold %s %s\n' %(p['Title'].encode('UTF-8'), groundtruth_title, '')
                compare.append((groundtruth_title, p['Title']))
                #self._compareBody(p['Body'], groundtruth)
                v = self._compareTitle(groundtruth_title, p['Title'])
                #print 'Accuracy ?' , v
                acc +=v
                self.WritePrediction(p, fid, foldername)
            acc/=len(urls)
            res.append(acc)
        print('Results')
        for x, y in compare:
            print (x)
            print (y)
            print (self._compareTitle(x, y))
            print ('-'*75)
        return res, sum(res)/len(res), len(self.set1)+len(self.set2)+len(self.set3)

    def getExamples(self):
        #csv and 
        urls = []
        fid = []
        td = open(self.trainfile)
        for each in td.readlines():
            k = each.strip().split(',');
            fid.append(k[0])
            urls.append(k[1])
        return urls, fid


    def _getExamples(self):
        fids_dict = {}
        for each in os.listdir(self.groundtruthpath+'/Title'):
            res = ''
            for every in each:
                if every == '.':
                    break;
                res+=every
            fids_dict[res] = 1

        print ("keys %s" %fids_dict)
        print (len(fids_dict))
        urls = []
        fid = []

        td = open(self.trainfile)
        for each in td.readlines():
            k = each.strip().split(',')
            #print k[0]
            if k[0] in fids_dict:
                urls.append(k[1])
                fid.append(k[0])
        return urls, fid

    #Need not be used
    def WritePrediction(self, result, fid, foldername):
        fname = self.trainpath+foldername+'/'+fid+'.cleantext'
        with open(fname, 'w') as fp:
            json.dump(result, fp, ensure_ascii=False)
        return

class Temp:
    def predict(self, url):
        g={}
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
