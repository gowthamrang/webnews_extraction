#run python 2 and get pretty_print
import plotly.plotly as py
from plotly.tools import FigureFactory as FF 
from inputoutput import IO

from readability_extraction import Readablility
from goose_extraction import GOOSE
from boilerpipe_extraction import BoilerPipe
if __name__ == '__main__':
    io = IO()
    bp = BoilerPipe()
    pr = Readablility()
    g = GOOSE()
    d = {}
    print 'Evaluating BoilerPipe'
    _,d['boilerpipe'],_ = io.evaluate((bp, 'boilerpipe'))
    print 'Evaluating Goose'
    _,d['goose'],_ = io.evaluate((g, 'goose'))
    print 'Evaluating Readablility'
    _,d['readability'],nfiles = io.evaluate((pr, 'readability'))
    print '-'*75
    print 'Method\t\taccuracy'
    for each in d:
        print '%s\t\t%.4f' %(each, d[each])
    print '%d' %nfiles

