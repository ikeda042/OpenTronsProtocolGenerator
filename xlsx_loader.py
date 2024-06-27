from openpyxl import Workbook, load_workbook


def index_to_cell(index: int) -> str:
    chars: list[str] = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
    ]
    return chars[index % 8] + str(index // 8 + 1)


workbook: Workbook = load_workbook(filename="template.xlsx")
worksheet = workbook.active

header, *rows = [row for row in worksheet.iter_rows(values_only=True)]

data: list[list[str | None]] = [[j for j in i[1:]] for i in rows]
data: list[str | None] = [item for sublist in data for item in sublist]

pick_up_from: list[str] = [
    index_to_cell(i) for i in range(len(data)) if data[i] is not None
]

print(pick_up_from)
