from . import item_node
from . import plate_node


class PlatesNode(item_node.ItemNode):
    def __init__(self, parent, name, attrs):
        item_node.ItemNode.__init__(self, parent, name, attrs)
        self.plates = {}

    def onEndElement(self, child, name):
        if name == "Plate":
            self.plates[child.metadata.get("Name")] = child
        else:
            item_node.ItemNode.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Plate":
            return plate_node.PlateNode
