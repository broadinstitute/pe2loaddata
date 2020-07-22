from . import item_node
from . import well_node


class WellsNode(item_node.ItemNode):
    def __init__(self, parent, name, attrs):
        item_node.ItemNode.__init__(self, parent, name, attrs)
        self.wells = {}

    def onEndElement(self, child, name):
        if name == "Well":
            self.wells[child.id] = child
        return item_node.ItemNode.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Well":
            return well_node.WellNode
        return item_node.ItemNode.get_class_for_name(self, name)
