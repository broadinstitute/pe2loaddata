from . import item_handler, entry_handler


class MapHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
        self.entry_dict = {}

    def onEndElement(self, child, name):
        if name == "Entry":
            channel_id = child.metadata['ChannelID']
            if channel_id not in self.entry_dict.keys():
                self.entry_dict[channel_id] = {}
            for key, value in child.entries[channel_id].items():
                self.entry_dict[channel_id][key] = value
        return item_handler.ItemHandler.onEndElement(self, child, name)
    
    def get_class_for_name(self, name):
        if name == "Entry":
            return entry_handler.EntryHandler
        return item_handler.ItemHandler.get_class_for_name(self, name)