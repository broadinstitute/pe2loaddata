from . import node
from . import plate_node


class PlatesNode(node.Node):
    def __init__(self, parent, name, attrs):
        node.Node.__init__(self, parent, name, attrs)
        self.plates = {}

    def onEndElement(self, child, name):
        if name == "Plate":
            self.plates[child.metadata.get("Name")] = child
        else:
            node.Node.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Plate":
            return plate_node.PlateNode
