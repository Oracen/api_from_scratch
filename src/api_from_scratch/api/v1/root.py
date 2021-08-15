from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def display_root():
    """
    Root function, shows default API response.

    Returns:
        Dict<str, str>: Hello world response
    """
    # TODO: Replace with API call tree
    return {"message": "TODO: Finish schema service"}
