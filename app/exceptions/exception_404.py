from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse

async def exception_404(request: Request, exc:HTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)
    if exc.detail == "Profile Not Found":
        return RedirectResponse('/profile/create')
    if exc.status_code == 404:
        return RedirectResponse('/not_found')

    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)