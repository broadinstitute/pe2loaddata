from . import item_node


class PlateNode(item_node.ItemNode):
    def __init__(self, parent, name, attrs):
        item_node.ItemNode.__init__(self, parent, name, attrs)
        self.well_ids = []

    def onEndElement(self, child, name):
        if name == "Well":
            self.well_ids.append(child.id)
        else:
            item_node.ItemNode.onEndElement(self, child, name)
