# Full Stack Trivia API Backend

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.
A virtual environment is advised to work in when using python.
After setting up your virtual environment and running, install dependencies by naviging to the `/backend` directory and use the command:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Backend

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=trivia
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

## Tests
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Hosting

Currently, this API is be hosted on the localhost of the development machine
`http://127.0.0.1:5000`

## API

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: unprocessable 


## Endpoints

GET Categories - `http://127.0.0.1:5000/categories` 
- Returns a list (json format) of all available categories
- *Result Example:*  

`curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```


GET `http://127.0.0.1:5000/questions?page={page_number}` 
- Returns the total lists of questions with 10 in a page
- *Result Example*
`curl http://127.0.0.1:5000/questions?page=3`  

 ``` {
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"currentCategory": "All",
"questions": [
{
"answer": "H2O",
"category": 1,
"difficulty": 1,
"id": 48,
"question": "Water Formula"
},
{
"answer": "physics",
"category": 1,
"difficulty": 1,
"id": 49,
"question": "What is universal"
}
],
"success": true,
"totalQuestions": 22
}
```

DELETE `http://127.0.0.1:5000/questions/{question_id}`
- Delete a questions from the available questions  
- *Result Example* 
`curl -X DELETE http://127.0.0.1:5000/questions/2`

```
{
  "deleted": "2", 
  "success": true
}
```

POST `http://127.0.0.1:5000/questions`
- Create a new question
- *Result Example* 

`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"A question", "answer":"AN answer", "category":"1", "difficulty":"1"}'`

```
{
  "created": 23, 
  "success": true
}
```
POST `http://127.0.0.1:5000/questions/search`
- Searches for a question from available questions
- *Result Example*
`curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"caged"}'`

```
{
  "current_category": "All", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitles 'I know why the caged bird sings'?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

GET `http://127.0.0.1:5000/categories/{category_id}/questions`
- Returns a list of questions based on the selected category number
- *Result Example:*

` curl http://127.0.0.1:5000/categories/1/questions`

```
{
"currentCategory": "Science",
"questions": [
{
"answer": "Alexander Fleming",
"category": 1,
"difficulty": 3,
"id": 21,
"question": "Who discovered penicillin?"
},
{
"answer": "Blood",
"category": 1,
"difficulty": 4,
"id": 22,
"question": "Hematology is a branch of medicine involving the study of what?"
},
{
"answer": "physics",
"category": 1,
"difficulty": 1,
"id": 49,
"question": "What is universal"
}
],
"success": true,
"totalQuestions": 3
}
```

POST `http://127.0.0.1:5000/quizzes`
- Returns one question at a time based on selected category to play a quiz
- *Result Example*

` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"id":"1", "type":"Science"}}'`

- set type to "all" and id to 0 to select all categories

```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```
