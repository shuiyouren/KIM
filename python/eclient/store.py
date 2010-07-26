import xml.dom.minidom, os
from base import *

class store:
    "Store Client data"
    def __init__(self ):
        pass

    def setDir (self, Dir ):
        "Set de Store base dir"
        self.baseDir = Dir

    def getData (self, dataName ):
        path = os.path.join( self.baseDir, 'eclient-data.xml')
        f = open( path, 'r' )
        Dxml = f.read()

        doc = xml.dom.minidom.parseString ( Dxml )
        
        try:
            data = doc.getElementsByTagName( dataName )[0].firstChild.nodeValue
        except:
            return ''
        else:
            return data
