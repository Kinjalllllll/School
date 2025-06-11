from email.message import  EmailMessage
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import List
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
import uvicorn




conf= ConnectionConfig(
    MAIL_USERNAME ="barotkinjal29@gmail.com",
    MAIL_PASSWORD = "qbtt dktc hbmm exfb",
    MAIL_FROM = "barotkinjal29@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)



html = """

"""


async def send_email(subject: str,recipients :list[str],body:str):

    message = MessageSchema(subject=subject,
                            recipients=recipients,
                            body=body,
                            subtype=MessageType.html
                            )
 

async def send_mail_template(subject: str, recipients: list[str], body_dict: dict, template_name: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=body_dict,
        subtype=MessageType.html
    )


async def send_email_with_attachments(subject: str, recipients: list[str], body: str, attachments: list):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html,
        attachments=attachments 
    )
    fm = FastMail(conf) # type: ignore
    await fm.send_message(message)










