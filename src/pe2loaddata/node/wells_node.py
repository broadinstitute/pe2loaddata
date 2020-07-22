from . import node
from . import well_node


class WellsNode(node.Node):
    def __init__(self, parent, name, attrs):
        node.Node.__init__(self, parent, name, attrs)
        self.wells = {}

    def onEndElement(self, child, name):
        if name == "Well":
            self.wells[child.id] = child
        return node.Node.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Well":
            return well_node.WellNode
        return node.Node.get_class_for_name(self, name)
