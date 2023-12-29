from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException

from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
from src.conf.config import config
from fastapi.security import OAuth2PasswordBearer
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.routing import Request
import os
import uvicorn
import cloudinary

from src.schemas import EmailSchema

load_dotenv()

app = FastAPI()


cloudinary.config(
    cloud_name=config.CLD_NAME,
    api_key=config.CLD_API_KEY,
    api_secret=config.CLD_API_SECRET,
    secure=True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_USERNAME,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME="TODO Systems",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

limiter = FastAPILimiter(
    key_func=lambda _: "global",  # Идентификатор для глобального обмеження
    redis_url="redis://localhost:6379/0",
)


@app.get("/contacts/", dependencies=[Depends(RateLimiter(times=5, minutes=1))])
async def read_contacts():
    """
    The read_contacts function returns a JSON object containing the message &quot;Read contacts&quot;.
    
    :return: A dictionary with a &quot;message&quot; key and the value of &quot;read contacts&quot;
    :doc-author: Trelent
    """
    return {"message": "Read contacts"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/user/contacts/", dependencies=[Depends(RateLimiter(times=5, minutes=1))])
async def read_user_contacts(token: str = Depends(oauth2_scheme)):
    """
    The read_user_contacts function is used to read the user's contacts.
        This function requires a valid access token.
    
    :param token: str: Get the token from the authorization header
    :return: {&quot;message&quot;: &quot;read user contacts&quot;}
    :doc-author: Trelent
    """
    return {"message": "Read user contacts"}


# Застосування глобального обмеження на швидкість для всіх маршрутів
@app.middleware("http")
async def limiter_middleware(request: Request, call_next):
    """
    The limiter_middleware function is a middleware function that initializes the limiter object,
        calls the next middleware in line (or the route handler if there are no more), and then closes
        out the limiter object. This allows us to use asyncio with our rate limiting.
    
    :param request: Request: Get the request object
    :param call_next: Pass the request to the next middleware in line
    :return: The response from the next middleware
    :doc-author: Trelent
    """
    await limiter.init()
    response = await call_next(request)
    await limiter.close()
    return response


# Додавання обробника помилок для обробки випадку перевищення обмежень
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    The http_exception_handler function is a custom exception handler that returns JSON instead of HTML for HTTP errors.
        Args:
            request (Request): The Request object.
            exc (HTTPException): An HTTPException instance, containing all the information about the error that occurred.
    
    :param request: Access the request object
    :param exc: Pass the exception object to the handler
    :return: A json response with the error
    :doc-author: Trelent
    """
    return {"error": exc.detail}


@app.post("/send-email")
async def send_in_background(
        background_tasks: BackgroundTasks,
        body: EmailSchema):
    """
    The send_in_background function sends an email in the background.
    
    :param background_tasks: BackgroundTasks: Add the task to the background tasks
    :param body: EmailSchema: Pass the email address to send the message to
    :return: {&quot;message&quot;: &quot;email has been sent&quot;}
    :doc-author: Trelent
    """
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}


@app.post("/upload-avatar/")
async def upload_avatar(file: UploadFile):
    """
    The upload_avatar function uploads an avatar to Cloudinary and returns the URL of the uploaded image.
    
    :param file: UploadFile: Get the file object from the request
    :return: A dictionary with the avatar_url key
    :doc-author: Trelent
    """
    # Отримати завантажене зображення
    contents = await file.read()

    # Завантажити зображення на Cloudinary
    response = upload(contents, folder="avatars")

    if response.get("public_id"):

        url, options = cloudinary_url(response["public_id"], format="png")
        return {"avatar_url": url}
    else:
        raise HTTPException(
            status_code=500, detail="Failed to upload avatar to Cloudinary"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)