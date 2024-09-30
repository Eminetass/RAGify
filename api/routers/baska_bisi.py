from fastapi import APIRouter

router_2 = APIRouter(
    prefix="/baska_bisi",
    tags=["baska_bisi"],
)


@router_2.get('/get_text')
def get_text():
    try:
        return '{"text": "Hello World"}'
    except Exception as e:
        return {'error': str(e)}

