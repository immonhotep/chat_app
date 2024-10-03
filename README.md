#Chat Application with social media features

A simple real-time ASGI chat application created with python & django channels. Code also contain necessary javascripts for real time communication. Frontend design made with free tailwind componets, and templates, and have minimalistic style.
Reason of the website: only for education or study, practise django, python and ASGI applications. 
Application made only with custom and generic class based views.

The application have possibility to create real time chat rooms, and private chat rooms as well for 2 users. Little social media features, allow to users connect each other, also have possiblity to create wsgi non-real time forums.

Application Functions:

User Functions:
- Registration, Login and, user profile update, change user password.

Forum fuctions:
- Create forums,update and delete own forums
- Create forum comments, edit or delete own comments and, report other user comments as well, function to reply comments
- Superuser can  hide reported comments or allow them
- Superuser have separate page to check reported comments overview

Chat functions:
-Create public chat rooms, edit or delete owned rooms.
-Connect to private chat rooms between two users who have connection relationship.

Social media features:
- list users
- Send invitation request to other users, ability to accept, or reject these requests
- list and review invitations requests.
- list user connections 
- ability to remove user from own connecion list ,
- ability to open private chat with users from our connection list.
- see our unread messages and set those to read this way hide them

Installation:

1. Clone the repository ( git clone https://github.com/immonhotep/chat_app.git )
2. Create virtual environment and activate it. (example on linux:  virtualenv venv  and source venv/bin/activate )
3. Install the necessary packages and django  ( pip3 install -r requirements.txt )
4. Make sure that media/images/default_user.jpg is exist  ( about lack of space image files excluded from the repo so copy your own here with the same name this is required for user profile default image. Without this application drop FileNotFoundError on new user registration)
5. Create the database:( python3 manage.py makemigrations and then python3 manage.py migrate )
6. Create a superuser ( python3 manage.py createsuperuser )
7. Run the application ( python3 manage.py runserver )
8. Start using the application





