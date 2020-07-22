from . import node


class WellNode(node.Node):
    def __init__(self, parent, name, attrs):
        node.Node.__init__(self, parent, name, attrs)
        self.image_ids = []

    def onEndElement(self, child, name):
        if name == "Image":
            self.image_ids.append(child.id)
        return node.Node.onEndElement(self, child, name)
