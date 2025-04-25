from fastapi import APIRouter


router = APIRouter(prefix="/ratings", tags=["Операции с оценками"])

@router.patch("/set_rating", status_code=status.HTTP_201_CREATED)
def set_rating():  #TODO
    pass

@router.get("/get_top", status_code=status.HTTP_200_OK)
def get_top():  #TODO
    pass

@router.get("/get_my_recommend", status_code=status.HTTP_200_OK)
def get_my_recommend():  #TODO
    pass