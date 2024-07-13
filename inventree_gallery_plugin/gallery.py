"""Sample implementation for ActionMixin."""

from plugin import InvenTreePlugin
from plugin.mixins import EventMixin, PanelMixin, ActionMixin, APICallMixin, SettingsMixin
from stock.views import StockItemDetail
from stock.models import StockItem, StockItemAttachment
from part.views import PartDetail
from part.models import Part, PartAttachment

class GalleryPlugin(PanelMixin, InvenTreePlugin):
    """An EXTREMELY simple action plugin which demonstrates the capability of the ActionMixin class."""

    NAME = 'AttachmentGalleryPlugin'
    SLUG = 'attachment_gallery'
    TITLE = 'AttachmentGallery'

    def is_image(self, attachment):
         return True

    def get_custom_panels(self, view, request):
            panels = []

            if isinstance(view, StockItemDetail) or isinstance(view, PartDetail):

                self.item=view.get_object()
                self.attachments = []

                if isinstance(self.item, StockItem):
                    item_attachments = StockItemAttachment.objects.filter(stock_item = self.item)

                if isinstance(self.item, Part):
                    item_attachments = PartAttachment.objects.filter(part = self.item)

                self.attachments = list(filter(lambda attachment: self.is_image(attachment), item_attachments))

                if len(self.attachments) > 0: 
                    panels.append({
                        'title': 'Attachment Gallery',
                        'icon': 'fa-paperclip',
                        'content_template': 'gallery/gallery.html',
                    })

            return panels