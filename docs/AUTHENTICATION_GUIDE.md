# User Authentication Guide

## Overview
User authentication has been successfully implemented in the IoTShield dashboard. Users can now register, login, and logout from the system.

## Features Implemented

### 1. **User Registration**
- URL: http://127.0.0.1:8000/register/
- Users can create new accounts with:
  - Username
  - Email
  - Password (with confirmation)
- Automatic login after successful registration
- Form validation:
  - Checks if passwords match
  - Checks if username already exists
  - Checks if email already registered

### 2. **User Login**
- URL: http://127.0.0.1:8000/login/
- Users can login with:
  - Username
  - Password
- Session-based authentication
- Redirects to dashboard after successful login

### 3. **User Logout**
- URL: http://127.0.0.1:8000/logout/
- Logs out the current user
- Redirects to login page

### 4. **Navigation Updates**
All pages (dashboard, devices, alerts) now show:
- **When logged out**: Login and Register buttons
- **When logged in**: 
  - "Welcome, [username]" message
  - Logout button

## Files Modified/Created

### New Templates
1. **dashboard/templates/login.html**
   - Beautiful login form with Tailwind CSS styling
   - Username and password fields
   - Link to registration page

2. **dashboard/templates/register.html**
   - Registration form with Tailwind CSS styling
   - Username, email, password, and confirm password fields
   - Link to login page

### Modified Files
1. **dashboard/views.py**
   - Added `login_view()` - handles user login
   - Added `register_view()` - handles user registration
   - Added `logout_view()` - handles user logout
   - Imported Django authentication functions

2. **dashboard/urls.py**
   - Added `/login/` route
   - Added `/register/` route
   - Added `/logout/` route

3. **dashboard/templates/dashboard.html**
   - Updated navigation bar to show login/register/logout buttons
   - Shows username when logged in

4. **dashboard/templates/devices.html**
   - Updated navigation bar with authentication buttons

5. **dashboard/templates/alerts.html**
   - Updated navigation bar with authentication buttons

## How to Use

### For New Users:
1. Go to http://127.0.0.1:8000/register/
2. Fill in username, email, and password
3. Click "Create Account"
4. You'll be automatically logged in and redirected to dashboard

### For Existing Users:
1. Go to http://127.0.0.1:8000/login/
2. Enter your username and password
3. Click "Sign in"
4. You'll be redirected to dashboard

### To Logout:
1. Click the "Logout" button in the navigation bar
2. You'll be logged out and redirected to login page

## Backend Authentication (API)

The backend also has REST API endpoints for authentication using JWT tokens:

- **Register API**: POST to `/api/auth/register/`
  ```json
  {
    "username": "yourname",
    "email": "your@email.com",
    "password": "yourpassword"
  }
  ```
  Returns JWT access and refresh tokens.

- **Login API**: POST to `/api/auth/login/`
  ```json
  {
    "username": "yourname",
    "password": "yourpassword"
  }
  ```
  Returns JWT access and refresh tokens.

## Next Steps

Now that authentication is implemented, the next tasks are:

1. ✅ **User login/authentication** - COMPLETED
2. ⏳ **Email alerts (Zoho Mail)** - Connect authenticated users to email notifications
3. ⏳ **ESP32 real hardware implementations** - Hardware integration

## Testing

To test the authentication:

1. **Register a new user:**
   - Visit http://127.0.0.1:8000/register/
   - Create a test account

2. **Login:**
   - Visit http://127.0.0.1:8000/login/
   - Use your credentials

3. **Check authenticated state:**
   - You should see "Welcome, [username]" in the navigation bar
   - Logout button should be visible

4. **Logout:**
   - Click logout button
   - You should be redirected to login page

## Admin Panel

You can also access the Django admin panel:
- URL: http://127.0.0.1:8000/admin/
- Username: anowar (your superuser account)
- You can manage users, devices, sensors, and alerts from here

## Notes

- All passwords are securely hashed using Django's built-in password hashing
- Sessions are handled by Django's session framework
- CSRF protection is enabled for all forms
- The authentication is ready for the next step: email notifications for logged-in users
