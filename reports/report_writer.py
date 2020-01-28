import datetime
import xlsxwriter
from mongoengine.queryset import QuerySet


def xlsx_report_writer(records, report_dict, filename):
    """
        This function writes a  report in xlsx format.

    Args:
        applications: Queryset to be evaluated & iterate over.
        report_dict: Dictionary for type of report we need to generate.
        filename: name of the report to be generated.


    Returns:
        Returns a  report.

    """
    xlsx_workbook = xlsxwriter.Workbook(filename)
    xlsx_worksheet = xlsx_workbook.add_worksheet()
    date_format = xlsx_workbook.add_format({"num_format": "yyyy-mm-dd"})
    bold = xlsx_workbook.add_format({"bold": 1})
    headers = list(report_dict.keys())
    for i, header in enumerate(headers):
        xlsx_worksheet.write(0, i, header, bold)

    if isinstance(records, QuerySet):
        records = records.no_cache()
    else:
        records = records

    # write files
    for row, record in enumerate(records):
        row = row + 1
        row_data = []
        for key, func in report_dict.items():
            if callable(func):
                value = func(record)
            else:
                value = func
            row_data.append(value)
        for col, val in enumerate(row_data):
            if isinstance(val, datetime.date):
                xlsx_worksheet.write(row, col, val, date_format)

            else:
                xlsx_worksheet.write(row, col, val)
    xlsx_workbook.close()
    return filename
