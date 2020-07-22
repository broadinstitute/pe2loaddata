from . import item_handler


class ImagesHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
        self.images = {}

    def onEndElement(self, child, name):
        if name == "Image":
            self.images[child.id] = child
        else:
            item_handler.ItemHandler.onEndElement(self, child, name)
