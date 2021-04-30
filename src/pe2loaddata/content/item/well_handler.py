from . import item_handler


class WellHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
        self.image_ids = []

    def onEndElement(self, child, name):
        if name == "Image":
            self.image_ids.append(child.id)
        return item_handler.ItemHandler.onEndElement(self, child, name)
