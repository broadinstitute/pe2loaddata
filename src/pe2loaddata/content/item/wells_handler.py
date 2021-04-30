from . import well_handler, item_handler


class WellsHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
        self.wells = {}

    def onEndElement(self, child, name):
        if name == "Well":
            self.wells[child.id] = child
        return item_handler.ItemHandler.onEndElement(self, child, name)

    def get_class_for_name(self, name):
        if name == "Well":
            return well_handler.WellHandler
        return item_handler.ItemHandler.get_class_for_name(self, name)
