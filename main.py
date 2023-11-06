from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from firebase import Firebase 
from datetime import datetime  
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from starlette.requests import Request
import sendgrid  
from sendgrid.helpers.mail import Mail, Email, Content
import random
import string

app = FastAPI()

# Initialize Firebase
firebase = Firebase() 

# Initialize rate limiting
limiter = FastAPILimiter(key_func=lambda request: request.client.host, rate_limit="10/minute")

# Models for input and response
class UserRegister(BaseModel):
    username: str
    email: str
    full_name: str

class UserProfile(BaseModel):
    username: str
    email: str
    full_name: str
    created_at: str  

# Function to generate a reset token (you need to implement this)
def generate_reset_token():
    token_length = 20
    characters = string.ascii_letters + string.digits
    reset_token = ''.join(random.choice(characters) for _ in range(token_length))
    return reset_token

# Function to send a password reset email
def send_password_reset_email(email: str, reset_token: str):
    sg = sendgrid.SendGridAPIClient(api_key="YOUR_SENDGRID_API_KEY")
    from_email = Email("your@email.com")
    to_email = Email(email)
    subject = "Password Reset Request"
    content = Content("text/plain", "Click this link to reset your password: reset-link.com/token=" + reset_token)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


@app.post("/register", response_model=UserProfile)
def register_user(user_data: UserRegister):
    try:
        # Validate and create user in Firebase Authentication
        user = firebase.register_user(user_data.email, user_data.password)

        # Store user details in Firestore
        user_profile = UserProfile(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            created_at=str(datetime.now())  # Store the current timestamp as a string
        )
        firebase.store_user_profile(user.uid, user_profile)

        return user_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login_user(email: str, password: str):
    try:
        # Authenticate the user using Firebase Authentication
        user = firebase.login_user(email, password)

        # Return a token or any other necessary response
        return {"token": user.token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/profile/{user_id}", response_model=UserProfile)
def get_user_profile(user_id: str):
    try:
        # Retrieve the user's profile from Firestore
        user_profile = firebase.get_user_profile(user_id)

        return user_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/profile/{user_id}", response_model=UserProfile)
def update_user_profile(user_id: str, user_data: UserRegister):
    try:
        # Update the user's profile in Firestore (you need to implement this)
        user_profile = UserProfile(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            created_at=str(datetime.now())  # Update the 'created_at' timestamp
        )
        updated_profile = firebase.update_user_profile(user_id, user_profile)

        return updated_profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/profile/{user_id}")
def delete_user_profile(user_id: str):
    try:
        # Delete the user's profile and Firebase Authentication account
        firebase.delete_user_profile(user_id)
        return {"message": "User profile deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
