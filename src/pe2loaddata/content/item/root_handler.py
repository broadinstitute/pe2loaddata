from . import plates_handler, wells_handler, item_handler, images_handler


class RootHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
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
            item_handler.ItemHandler.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Plates":
            return plates_handler.PlatesHandler
        elif name == "Wells":
            return wells_handler.WellsHandler
        elif name == "Images":
            return images_handler.ImagesHandler
        else:
            return item_handler.ItemHandler.get_class_for_name(self, name)