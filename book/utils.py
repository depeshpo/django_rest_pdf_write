import csv
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from openpyxl import Workbook

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def export_to_csv(queryset, fields, file_name):
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
    # the csv writer
    writer = csv.writer(response)
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    writer.writerow(headers)

    # write data rows
    for item in queryset:
        writer.writerow([getattr(item, field) for field in headers])
    return response


export_to_csv.short_description = "Download selected as csv"


def export_to_excel(queryset, **kwargs):
    field_names = kwargs['field_names']
    file_name = kwargs['file_name']
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename={file_name}.xlsx'.format(file_name=file_name)
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Books'

    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(field_names, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    # Iterate over all books
    for book in queryset:
        row_num += 1
        row = [
            book.id,
            book.name,
            book.author,
            book.created,
            book.detail.detail
        ]
        # Writing each record in new a row
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    workbook.save(response)
    return response
