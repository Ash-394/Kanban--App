# Kanban Application
###  Reference
-  *[Kanban](https://en.wikipedia.org/wiki/Kanban_board)* on Wikipedia

## Terms
- Board - Kanban board
- List - List of tasks
- Card - Each task is represented as a card
- Movement - Card can be moved from one list to another list
- Summary - Shows how the user is performing across lists based on the completed flag, time when it completed, it also shows graphs


## Features
- Used for tracking tasks
- User can have multiple lists
- Each list will have:
    1. ID
    2. Name
- User can add one or more cards to a list. Each card will have
    1. Title
    2. Content
    3. Deadline
    4. Completed flag


- System will also automatically capture task completed datetime
- System will track progress over time and shows graphs trend lines etc. as Summary

## Functionality
- User login
- Main Board with Lists
- List management
- Card management
- Summary page

## How to run
- Clone this repo or download it as a zip folder
- Open terminal inside the folder
- To install all the packages present in requirements.txt use command:
    -  ` pip install -r requirements.txt `

- After all the packages are installed, run the app by using the command:
    - ` python main.py `

- Once the app is started we can click on the url generated where the server is running. 

- It will redirect to login page. Go to the sign in page and a create username and password. Then login.

- Once logged in, there is a dashboard where we can view all of our tasks and lists and we can add new tasks and lists

- We can edit /delete tasks and lists

- The 'Summary' option  will take you to summary page where we have the summary of all the tasks

- Once you are done click on logout to get out of the session
