from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Операции с пользователями"])

@router.post("/create_user")
def create_user(): #TODO
    pass

@router.delete("/delete_user")
def delete_user(): #TODO
    pass