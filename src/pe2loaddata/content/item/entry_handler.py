from . import item_handler


class EntryHandler(item_handler.ItemHandler):
    def __init__(self, parent, name, attrs):
        item_handler.ItemHandler.__init__(self, parent, name, attrs)
        self.entries = {}

    def onEndElement(self, child, name):
        channel_id = self.metadata['ChannelID']
        if channel_id not in self.entries.keys():
            self.entries[channel_id]={}
        self.entries[channel_id][child.name]=child.content
        return item_handler.ItemHandler.onEndElement(self, child, name)