from . import item_handler


class PlateHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
        self.well_ids = []

    def onEndElement(self, child, name):
        if name == "Well":
            self.well_ids.append(child.id)
        else:
            item_handler.ItemHandler.onEndElement(self, child, name)
