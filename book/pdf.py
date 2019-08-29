from weasyprint import HTML
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView


class PDFTemplateResponse(TemplateResponse):

    def __init__(self, filename=None, *args, **kwargs):
        kwargs['content_type'] = "application/pdf"
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        disposition = 'attachment'
        if filename:
            self['Content-Disposition'] = '{}; filename="{}"'.format(disposition, filename)
        else:
            self['Content-Disposition'] = disposition

    @property
    def rendered_content(self):
        """Returns the rendered pdf"""
        html = super(PDFTemplateResponse, self).rendered_content
        base_url = self._request.build_absolute_uri("/")
        pdf = HTML(string=html, base_url=base_url).write_pdf()
        return pdf


class PDFTemplateResponseMixin(TemplateResponseMixin):
    response_class = PDFTemplateResponse
    filename = None

    def get_filename(self):
        """
        Returns the filename of the rendered PDF.
        """
        return self.filename

    def render_to_response(self, *args, **kwargs):
        """
        Returns a response, giving the filename parameter to PDFTemplateResponse.
        """
        kwargs['filename'] = self.get_filename()
        return super(PDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)


class PDFTemplateView(TemplateView, PDFTemplateResponseMixin):
    pass
