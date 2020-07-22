from . import node


class PlateNode(node.Node):
    def __init__(self, parent, name, attrs):
        node.Node.__init__(self, parent, name, attrs)
        self.well_ids = []

    def onEndElement(self, child, name):
        if name == "Well":
            self.well_ids.append(child.id)
        else:
            node.Node.onEndElement(self, child, name)
