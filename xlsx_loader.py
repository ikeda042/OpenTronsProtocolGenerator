from openpyxl import load_workbook

workbook = load_workbook(filename="template.xlsx")
worksheet = workbook.active


header, *rows = [row for row in worksheet.iter_rows(values_only=True)]

cols: dict[str, str] = {}
