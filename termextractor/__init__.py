# $Id$

# http://pypi.python.org/pypi/topia.termextract/

from APIApp import APIApp
from topia.termextract import extract
from topia.termextract import tag

class termextractor (APIApp) :

    def __init__ (self) :

        APIApp.__init__(self, 'xml')

        tagger = tag.Tagger()
        tagger.initialize()
        
        self.ex = extract.TermExtractor(tagger)
        self.ex.filter = extract.permissiveFilter

class Main (termextractor) :

    def get (self) :

        host = self.request.host_url
        url = "%s/terms?text=this is the network of our disconnect" % host
        
        self.response.out.write("Usage: <em>GET or POST</em> ")
        self.response.out.write("<a href=\"%s\">%s</a>" % (url, url))
        self.response.out.write(" (<a href=\"%s&format=json\">&format=json</a>)" % url)

        return
    
class Terms (termextractor) :

    def get (self) :
        return self.extract()

    def post (self) :
        return self.extract()

    def extract(self, text='') :

        text = self.request.get('text')

        if text == '' :
            self.api_error(1, 'Required input missing')
            return

        res = self.ex(text)
        terms = { 'query' : text, 'term' : [ ] }

        for r in res :
            
            terms['term'].append({'value' : r[0], 'occurrence' : r[1], 'strength' : r[1]})
            
        self.api_ok({'terms' : terms})
        return
