from requests import get
from libextract.api import extract

r = get('http://en.wikipedia.org/wiki/Information_extraction')
textnodes = list(extract(r.content))

import sys
reload(sys)
sys.setdefaultencoding('utf-8')



from IO import IO
	
class libextract:
	def __init__(self):
		pass

	def predict(self,url):
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
		if d['Title'] == None:
			d['Title'] = ''

		return d
		
			




if __name__ == '__main__':
	io = IO()
	rb = Readablility()
	accuracies = io.Evaluate((rb,'readability'))
	print accuracies
	