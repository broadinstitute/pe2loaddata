from . import item_node


class ImagesNode(item_node.ItemNode):
    def __init__(self, parent, name, attrs):
        item_node.ItemNode.__init__(self, parent, name, attrs)
        self.images = {}

    def onEndElement(self, child, name):
        if name == "Image":
            self.images[child.id] = child
        else:
            item_node.ItemNode.onEndElement(self, child, name)