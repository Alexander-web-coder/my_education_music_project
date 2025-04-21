from fastapi import APIRouter

router = APIRouter(prefix="/tracks", tags=["Операции с треками"])

@router.get("/get_full_list")
def get_full_list(): #TODO
    pass

@router.get("/get_top")
def get_top(): #TODO
    pass

@router.get("/get_my_recommend")
def get_my_recommend(): #TODO
    pass

@router.post("/create_track")
def create_track(): #TODO
    pass

@router.patch("/set_rating")
def set_rating(): #TODO
    pass

@router.delete("/delete_track")
def delete_track(): #TODO
    pass