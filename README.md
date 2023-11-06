# User Management using FastAPI

This project is a FastAPI-based user management system that integrates with Firebase for authentication and Firestore for user profile storage. It also includes functionality for sending password reset emails via SendGrid.

# Setup Instructions
Python installed on your system.
FastAPI and Firebase Admin SDK installed using pip.
Create a Firebase project on the Firebase Console.
Generate a private key for your Firebase project and download the JSON file.

# Installation
Clone this repository to your local machine.
Install the required dependencies: pip install fastapi firebase-admin sendgrid

# Running the Application
Start the FastAPI application using the following command: uvicorn main:app --reload

# Endpoints
/register (POST): Register a new user.
/login (POST): Log in a user.
/profile/{user_id} (GET): Retrieve user profile by user ID.
/profile/{user_id} (PUT): Update user profile by user ID.
/profile/{user_id} (DELETE): Delete user profile by user ID.
/reset-password (POST): Request a password reset email.

# Password reset functionality
The /reset-password endpoint allows users to request a password reset email. A unique reset token will be generated, sent to the user's email, and associated with the user's email address for verification.

# Rate limiting
Rate limiting is implemented on the API endpoints using the fastapi-limiter package. By default, there is a rate limit of 10 requests per minute per client host.
