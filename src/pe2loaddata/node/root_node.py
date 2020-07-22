from . import item_node
from . import images_node
from . import plates_node
from . import wells_node


class RootNode(item_node.ItemNode):
    def __init__(self, parent, name, attrs):
        item_node.ItemNode.__init__(self, parent, name, attrs)
        self.images = None
        self.plates = None
        self.wells = None

    def onEndElement(self, child, name):
        if name == "Images":
            self.images = child
        elif name == "Plates":
            self.plates = child
        elif name == "Wells":
            self.wells = child
        else:
            item_node.ItemNode.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Plates":
            return plates_node.PlatesNode
        elif name == "Wells":
            return wells_node.WellsNode
        elif name == "Images":
            return images_node.ImagesNode
        else:
            return item_node.ItemNode.get_class_for_name(self, name)