import xml.sax

from src.pe2loaddata.node import root_node


class DocumentNode(xml.sax.handler.ContentHandler):
    def startDocument(self):
        self.root = None

    def startElement(self, name, attrs):
        if self.root is None:
            self.root = root_node.RootNode(self, name, attrs)
            self.current_element = self.root
        else:
            self.current_element = self.current_element.onStartElement(
                name, attrs)

    def characters(self, content):
        self.current_element.characters(content)

    def endElement(self, name):
        self.current_element.endElement(name)
        self.current_element = self.current_element.parent

    def onEndElement(self, child, name):
        pass
