import xml.sax.handler


class ItemHandler(xml.sax.handler.ContentHandler):
    """Ignore all content until endElement"""

    def __init__(self, parent, name, attrs):
        super().__init__()
        self.parent = parent
        self.name = name
        self.content = ""
        self.metadata = dict(attrs)

    def onStartElement(self, name, attrs):
        return self.get_class_for_name(name)(self, name, attrs)

    def characters(self, content):
        self.content += content.strip()

    def endElement(self, name):
        self.parent.onEndElement(self, name)
        return self.parent

    def onEndElement(self, child, name):
        self.metadata[name] = child.content

    def get_class_for_name(self, name):
        return ItemHandler

    @property
    def id(self):
        return self.metadata["id"]

    @property
    def well_name(self):
        """The well name

        Taken from row and column metadata values, valid for Well and Image
        elements
        """
        row = int(self.metadata["Row"])
        col = int(self.metadata["Col"])
        return chr(ord('A') + row - 1) + ("%02d" % col)

    @property
    def channel_name(self):
        """The channel name

        Strip out spaces in the channel name because XML parser seems to
        be broken
        """
        try:
            channel = self.metadata["ChannelName"]
            return channel.replace(" ", "")
        except:
            return False

    @property
    def channel_id(self):
        """The integer channel id
        """
        channel = self.metadata["ChannelID"]
        return channel
