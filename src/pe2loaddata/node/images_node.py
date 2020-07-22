from . import node


class ImagesNode(node.Node):
    def __init__(self, parent, name, attrs):
        node.Node.__init__(self, parent, name, attrs)
        self.images = {}

    def onEndElement(self, child, name):
        if name == "Image":
            self.images[child.id] = child
        else:
            node.Node.onEndElement(self, child, name)