from fastapi import APIRouter, status


router = APIRouter(prefix="/tracks", tags=["Операции с треками"])


@router.get("/get_full_list", status_code=status.HTTP_200_OK)
def get_full_list():  #TODO
    pass


@router.get("/get_top", status_code=status.HTTP_200_OK)
def get_top():  #TODO
    pass


@router.get("/get_my_recommend", status_code=status.HTTP_200_OK)
def get_my_recommend():  #TODO
    pass


@router.post("/create_track", status_code=status.HTTP_201_CREATED)
def create_track():  #TODO
    pass


@router.patch("/set_rating", status_code=status.HTTP_202_CREATED)
def set_rating():  #TODO
    pass


@router.delete("/delete_track", status_code=status.HTTP_204_NO_CONTENT)
def delete_track():  #TODO
    pass
