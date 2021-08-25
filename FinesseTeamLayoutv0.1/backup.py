import os
from xml.sax.saxutils import escape,unescape

class backup(object):

    @classmethod
    def output_to_file(cls,Name,xmlstring,publisher):
        try:
            newxmlstring = backup.xmlesc(xmlstring)
            file_name = Name + ".xml"
            save_path = os.getcwd() + "/XMLFolder"
            completeName = os.path.join(save_path, file_name)
            if not os.path.isdir(save_path):
                os.mkdir(save_path)
            with open(completeName, 'w') as f:
                f.write(newxmlstring)
            resp_file_name = "##### file written  succesfully ##### %s" % (file_name)
            return  resp_file_name
        except Exception as e:
            err = "##### error while writing file %s" %(e)
            return(err)

    @classmethod
    def xmlesc(cls,txt):
        return unescape(txt, entities={"&lt;": "<","&gt;":">","&amp;":"&", "&apos;":"\'", "&quot;": "\""})
