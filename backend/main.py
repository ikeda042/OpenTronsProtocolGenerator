import aiofiles
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8080",
]


app = FastAPI()
router_dev = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router_dev.get("/xlsx_template")
async def xlsx_template():
    return FileResponse("dev/template.xlsx")


class Values(BaseModel):
    values: list[str]


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


async def update_template_file(
    pick_up_from: list[str], template_file_path: str, output_file_path: str
) -> None:
    async with aiofiles.open(template_file_path, "r") as file:
        template_code = await file.read()

    pick_up_from_assignment = f"self.pick_up_from: list[str] = {pick_up_from}"
    updated_code = template_code.replace(
        "self.pick_up_from: list[str] = []", pick_up_from_assignment
    )

    async with aiofiles.open(output_file_path, "w") as file:
        await file.write(updated_code)


async def create_csv(tags: list[str]) -> None:
    rows, cols = 8, 12
    csv_string = ""

    for i in range(rows):
        row = []
        for j in range(cols):
            index = i * cols + j
            if index < len(tags):
                row.append(tags[index])
            else:
                row.append("")
        csv_string += ",".join(row) + "\n"

    async with aiofiles.open("backend/result.csv", "w") as file:
        await file.write(csv_string)


@router_dev.post("/submit-values/")
async def submit_values(values: Values):
    valid_values = []
    valid_tags = []
    for i in enumerate(values.values):
        if i[1] != "":
            valid_values.append(index_to_cell(i[0]))
            valid_tags.append(i[1])
    await update_template_file(
        valid_values, "backend/template.py", "backend/return_template.py"
    )
    await create_csv(valid_tags)
    return {"values": valid_values}


@router_dev.get("/return-template/")
async def return_template():
    return FileResponse("backend/return_template.py")


app.include_router(router_dev)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
