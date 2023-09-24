from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr, BaseModel
from app.auth.secrets import secrets
from fastapi.templating import Jinja2Templates

class EmailSchema(BaseModel):
    email: EmailStr

conf = ConnectionConfig(**secrets['EMAIL'])
fm = FastMail(conf)

def email_subject(_type:str = None):
    if _type == "verify":
        return "Verify Account"
    
    if _type == "forgot":
        return "Forgot Password"
    
    return "Caloria Email"


def template_name(_type:str=None):
    if _type == "verify":
        return "verification"
    
    if _type == "forgot":
        return "forgot_password"
    
    return "Caloria Email"
    
async def send_email(email: EmailSchema, request: Request, _type:str = None, token:str = None) -> JSONResponse:
    subject = email_subject(_type=_type)
    if request is None:
        message = MessageSchema(
            subject=subject,
            recipients=[email.email],
            # template_body={"link": request.base_url},
            subtype="html")
        await fm.send_message(message)

    else:
        url = 'reset-password' if _type == "forgot" else "verify"
        token_str = f"?token={token}" if token is not None else "" 
        link = f"{request.base_url}{url}{token_str}"
        message = MessageSchema(
            subject=subject,
            recipients=[email.email],
            template_body={"link": link},
            subtype=MessageType.html)


        await fm.send_message(message, template_name=f"email/{template_name(_type=_type)}.html")
    return JSONResponse(status_code=200, content={"message": "email has been sent"})