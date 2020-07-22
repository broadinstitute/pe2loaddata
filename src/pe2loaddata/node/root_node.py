from . import node
from . import images_node
from . import plates_node
from . import wells_node


class RootNode(node.Node):
    def __init__(self, parent, name, attrs):
        node.Node.__init__(self, parent, name, attrs)
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
            node.Node.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Plates":
            return plates_node.PlatesNode
        elif name == "Wells":
            return wells_node.WellsNode
        elif name == "Images":
            return images_node.ImagesNode
        else:
            return node.Node.get_class_for_name(self, name)