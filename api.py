from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from db.models import StraightSofas
from schemas import InfoModelBase, InfoModelOut, UpdateInfoModel

router = APIRouter()


@router.get("/", response_model=list[InfoModelOut])
async def get_info(page: int = 1, page_size: int = 10):
    data = await StraightSofas.objects.paginate(page, page_size).all()
    return data


@router.get("/{title}", response_model=list[InfoModelOut])
async def get_info_by_title(title: str):
    return await (
        StraightSofas.objects.filter(StraightSofas.title.icontains(title)).all()
    )


@router.post("/", response_model=InfoModelOut, status_code=201)
async def add_info(data: InfoModelBase):
    return await StraightSofas(**data.dict()).save()


@router.put("/{id_}", response_model=InfoModelOut)
async def update_info(id_: int, data: UpdateInfoModel):
    """Delete the lines you don't want to be changed"""
    data = data.dict(exclude_unset=True, exclude_defaults=True)
    exists = await StraightSofas.objects.get_or_none(pk=id_)
    if not exists:
        raise HTTPException(status_code=404)
    return await exists.update(**data)


@router.delete("/{id_}")
async def delete_info(id_: int):
    exists = await StraightSofas.objects.get_or_none(pk=id_)
    if not exists:
        raise HTTPException(status_code=404)
    await exists.delete()
    return JSONResponse(status_code=200, content="OK")
