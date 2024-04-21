# ForumApp

## Description
ForumApp is a web-based discussion platform that allows users to engage and start discussion threads.

## Key Features

- **Registration and Login:** Users can create their own account and log in to the application.
- **Browsing Discussion Areas:** Users can view a list of all discussion threads on the homepage.
- **Creating Threads:** Users can start a new discussion thread in a selected discussion area.
- **Posting Messages:** Users can reply to existing threads by posting messages.
- **Editing/Deleting Messages and Threads:** Users can edit or delete their own messages and threads.
- **Message Search:** Users can search for messages containing specific words or phrases.

## Installation
### 1. Git clone the ForumApp repository
- Open your terminal and run the following command: git clone `https://github.com/YourUsername/ForumApp.git`
### 2. Set Up a Virtual Environment
- In terminal run command: python3 -m venv venv
- Next in terminal run: source venv/bin/activate or alternatively on Windows use: source venv\Scripts\activate
### 3. Install Dependencies
- pip install -r requirements.txt
### 4. Create .env File
- Create .env file in the root directory of the project 
- Open the .env file in a text editor and add the following lines:
  - DATABASE_URL=`postgres://postgres.gwgcixzhhbqwhqifqbaf:hR84vPLD#M52pj5@aws-0-eu-central-1.pooler.supabase.com:5432/postgres`
  - SECRET_KEY='your_secret_key'
    - If you don't have one, you can create one with the following command in terminal: ´export SECRET_KEY='temporary'´. Now add SECRET_KEY=temporary to the .env file.
### 5. Run the Application
- In terminal run the following command: python3 app.py


# Update 1 (Välipalautus 2)

- **Registration and Login:** Users can now register their own accounts and log in to the application.
- **Creating Threads:** Users can start a new thread.
- **Posting Messages:** Users can comment threads.
- **Database solution:** Database is implemented using postresql and supabase cloud services.

# Update 2 (Välipalautus 3)

- **SQL Queries:** Transitioned all database interactions to SQL queries.
- **.gitingore:** Updated .gitignore to exclude sensitive files.
- **Libraries:** Added requirements.txt with all necessary libraries.





