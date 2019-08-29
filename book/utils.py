import csv
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def populate_from_csv(queryset, file_name):
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download
    response['Content-Disposition'] = 'attachment;filename=%s' % file_name
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write firs row with header information
    writer.writerow(field_names)
    # write data rows
    for item in queryset:
        writer.writerow([getattr(item, field) for field in field_names])
    return response


populate_from_csv.short_description = "Download selected as csv"
