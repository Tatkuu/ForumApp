# ForumApp

## Description
ForumApp is a web-based discussion platform that allows users to engage and start discussion threads.

# Final Version Features
- **Registration and Login:** Users can register their own accounts and log in to the application.
- **Creating Threads:** Users can start a new thread.
- **Posting Messages:** Users can reply to existing threads by posting messages.
- **Database Solution:** Database is implemented using SQL queries and supabase cloud services.
- **Editing/Deleting Messages:** Users can edit or delete their own messages.
- **Thread Search:** Users can search threads.
- **Thread List:** List of threads shows on the main page. 

## Installation
### 1. Git clone the ForumApp repository
- Open your terminal and run the following command: git clone `https://github.com/YourUsername/ForumApp.git`
### 2. Set Up a Virtual Environment
- In terminal run command: `python3 -m venv venv`
- Next in terminal run: `source venv/bin/activate` or alternatively on Windows use: `source venv\Scripts\activate`
### 3. Install Dependencies
- In terminal run the following: `pip install -r requirements.txt`
### 4. Create .env File
- Create .env file in the root directory of the project 
- Open the .env file in a text editor and add the following lines:
  - DATABASE_URL=`postgres://postgres.gwgcixzhhbqwhqifqbaf:hR84vPLD#M52pj5@aws-0-eu-central-1.pooler.supabase.com:5432/postgres`
  - SECRET_KEY='your_secret_key'
    - If you don't have one, you can create temporary secret key with the following command in terminal: `export SECRET_KEY='temporary'`. Now add `SECRET_KEY=temporary` to the .env file.
### 5. Run the Application
- In terminal run the following command: `python3 app.py`
