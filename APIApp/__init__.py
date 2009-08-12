from google.appengine.ext import webapp
from django.utils import simplejson
from django.utils import html
import types

class APIApp (webapp.RequestHandler) :

    def __init__ (self, default_format='xml') :
        
        webapp.RequestHandler.__init__(self)
                        
        self.format = default_format
        self.valid_formats = ('xml', 'json')
        
    def ensure_args(self, required) :
    
        for r in required :
            if not self.request.get(r) :
                self.api_error(1, 'required parameter missing: %s' % r)
                return False

        return True

    def api_error (self, code=999, msg='INVISIBLE ERROR') :
        out = {'stat' : 'fail', 'error' : { 'code' : code, 'message' : msg } }  
        self.send_rsp(out)
    
    def api_ok (self, out={}) :
        out['stat'] = 'ok'
        self.send_rsp(out)
  
    def send_rsp (self, data) :

        format = self.request.get('format')

        if format != '' and format in self.valid_formats :
            self.format = format
        
        rsp = self.serialize_rsp('rsp', data)
        
        if self.format == 'json' :
            return self.send_json(rsp)

        return self.send_xml(rsp)
  
    def send_json (self, json) :

        # because it's my bloody toy. see also:
        # http://simonwillison.net/2009/Feb/6/json/

        type = 'text/plain'

        if self.request.get('dtrt') :
            type = 'application/json'

        self.response.headers["Content-Type"] = type
        self.response.out.write(json)
    
    def send_xml (self, xml) :
        self.response.headers["Content-Type"] = "text/xml"
        self.response.out.write("<?xml version=\"1.0\" ?>")
        self.response.out.write(xml)

    def serialize_rsp (self, root, data) :

        if self.format == 'json' :
            return self.serialize_json(root, data)

        return self.serialize_xml(root, data)

    def serialize_json (self, root, data) :
        return simplejson.dumps({root : data})
    
    def serialize_xml (self, root, data) :
    
        xml = ''
        ima = type(data)

        if ima == types.DictType :

            xml += "<%s" % self.prepare_xml_content(root)

            attrs = []
            children = []
            cdata = None
        
            for (foo, bar) in data.items() :

                if foo == '_content' :
                    cdata = bar
                    break
                elif type(bar) != types.DictType and type(bar) != types.ListType :
                    attrs.append((foo, bar))
                else :
                    children.append((foo, bar))

                if cdata :
                    xml += ">%s</%s>" % (self.prepare_xml_content(cdata), self.prepare_xml_content(root))
                    return xml
        
            for pair in attrs :
                xml += self.serialize_xml(pair[0], pair[1])

            if len(children) == 0 :
                xml += " />"
                return xml
        
            xml += ">"

            for pair in children :
                xml += self.serialize_xml(pair[0], pair[1])
                        
            xml += "</%s>" % self.prepare_xml_content(root)
        
        elif ima == types.ListType :

            for item in data :
                xml += self.serialize_xml(root, item)

        else :

            xml += " %s=\"%s\"" % (self.prepare_xml_content(root), self.prepare_xml_content(data))

        return xml

    # will this some day fuck up an element name? oh, probably...
    
    def prepare_xml_content (self, data) :
        return html.escape(unicode(data))
