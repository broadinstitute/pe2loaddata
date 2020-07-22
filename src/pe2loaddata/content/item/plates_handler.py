from . import plate_handler, item_handler


class PlatesHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
        self.plates = {}

    def onEndElement(self, child, name):
        if name == "Plate":
            self.plates[child.metadata.get("Name")] = child
        else:
            item_handler.ItemHandler.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Plate":
            return plate_handler.PlateHandler
