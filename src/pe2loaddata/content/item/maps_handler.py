from . import item_handler, map_handler


class MapsHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
        self.map_dict = {}

    def onEndElement(self, child, name):
        if name == "Map":
            for channel_id, channel_entry in child.entry_dict.items():
                if channel_id not in self.map_dict.keys():
                    self.map_dict[channel_id]={}
                for key, value in channel_entry.items():
                    self.map_dict[channel_id][key] = value
        return item_handler.ItemHandler.onEndElement(self, child, name)
    
    def get_class_for_name(self, name):
        if name == "Map":
            return map_handler.MapHandler
        return item_handler.ItemHandler.get_class_for_name(self, name)