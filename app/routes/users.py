from fastapi import APIRouter, status

router = APIRouter(prefix="/users", tags=["Операции с пользователями"])

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(): #TODO
    pass

@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(): #TODO
    pass