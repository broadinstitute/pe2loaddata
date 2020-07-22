from . import item_node


class WellNode(item_node.ItemNode):
    def __init__(self, parent, name, attrs):
        item_node.ItemNode.__init__(self, parent, name, attrs)
        self.image_ids = []

    def onEndElement(self, child, name):
        if name == "Image":
            self.image_ids.append(child.id)
        return item_node.ItemNode.onEndElement(self, child, name)
