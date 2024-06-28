import aiofiles
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI

app = FastAPI()
router_dev = APIRouter()


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


@router_dev.post("/submit-values/")
async def submit_values(values: Values):
    valid_values = []
    for i in enumerate(values.values):
        if i[1] != "":
            valid_values.append(index_to_cell(i[0]))
    await update_template_file(
        valid_values, "backend/template.py", "backend/return_template.py"
    )
    return {"values": valid_values}


@router_dev.get("/return-template/")
async def return_template():
    return FileResponse("dev/return_template.py")


app.include_router(router_dev)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
