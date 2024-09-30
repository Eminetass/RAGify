from fastapi import APIRouter

from api.configs.constants import ErrorMessages, StatusCodes

router = APIRouter(
    prefix="/ragify",
    tags=["ragify"],
)


@router.get('/get_text')
def get_text():
    try:
        return f'{"text": "Hello World","Status": {StatusCodes.SUCCESS}}'
    except Exception as e:
        return {'error': f'{str(e)} - {ErrorMessages.VALIDATION_ERROR}'}

