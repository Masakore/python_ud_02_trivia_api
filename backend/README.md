# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server
From within the `./src` directory first ensure you are working using your created virtual environment.  
To run the server, execute
```bash
flask run --reload
```

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns all available categories, success value.
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
"categories": {
      'categories': { 
      '1' : "Science",
      '2' : "Art",
      '3' : "Geography",
      '4' : "History",
      '5' : "Entertainment",
      '6' : "Sports" }
}, 
"success": true
}
```

#### GET /questions?page=${integer}
- General:
    - Returns a list of questions, success value, total number of books, all available categories, and current category
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions?page=2`
```
{
  "questions": [
    {
      'id': 10,
      'question': 'This is a question1',
      'answer': 'This is an answer1', 
      'difficulty': 5,
      'category': 1
    },
    {
      'id': 15,
      'question': 'This is a question2',
      'answer': 'This is an answer2', 
      'difficulty': 2,
      'category': 2
    },
    {
      'id': 21,
      'question': 'This is a question3',
      'answer': 'This is an answer3', 
      'difficulty': 3,
      'category': 4
    },
  ],
  "total_questions": 3,
  "categories": {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" 
  }, 
  "current_category": 1,
  "success": True
}
```

#### GET /categories/${category_id}/questions
- General:
    - Returns a list of questions based on a category you choose and current page number to update the frontend, success value, and total number of questions. 
- Sample: `curl http://127.0.0.1:5000/categories/1/questions?page=1`

``` {
  "questions": [
    {
      'id': 1,
      'question': 'This is a question1',
      'answer': 'This is an answer1', 
      'difficulty': 5,
      'category': 1
    },
    {
      'id': 15,
      'question': 'This is a question2',
      'answer': 'This is an answer2', 
      'difficulty': 2,
      'category': 1
    },
    {
      'id': 21,
      'question': 'This is a question3',
      'answer': 'This is an answer3', 
      'difficulty': 3,
      'category': 1
    },
  ],
  "total_questions": 3,
  "current_category": 1,
  "success": True
}
```

#### POST /quizzes
- General:
    - This endpoint should take category and previous question parameters and return a random questions within the given category and success value.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":"[1,2,3]", "quiz_category":"3"}`

``` {
  "question": {
      'id': 1,
      'question': 'This is a question1',
      'answer': 'This is an answer1', 
      'difficulty': 5,
      'category': 3
  },
  "success": True
}
```

#### POST /questions
1. **Create a new question**
    - Creates a new question using the submitted question, answer, category and difficulty. Returns True if success. 
- Sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the host city of olympic game in 2020", "answer":"Tokyo", "category":"2", "difficulty":"4"}'`
```
{
  "success": True
}
```

2. **Search questions**
    - Return success value, the number of total questions, a current category, and questions including a search term(case insensitive) passed as a parameter based on current page number to update the frontend.
- Sample `curl http://127.0.0.1:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"searchTerm":"This" }'`
```
{
  "questions": [
    {
      'id': 1,
      'question': 'This is a question1',
      'answer': 'This is an answer1', 
      'difficulty': 5,
      'category': 1
    },
    {
      'id': 15,
      'question': 'This is a question2',
      'answer': 'This is an answer2', 
      'difficulty': 2,
      'category': 1
    },
    {
      'id': 21,
      'question': 'This is a question3',
      'answer': 'This is an answer3', 
      'difficulty': 3,
      'category': 1
    },
  ],
  "total_questions": 3,
  "current_category": 1,
  "success": True
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/books/16?page=2`
```
{
  "deleted": 2,
  "questions": [
    {
      'id': 1,
      'question': 'This is a question1',
      'answer': 'This is an answer1', 
      'difficulty': 5,
      'category': 1
    },
    {
      'id': 3,
      'question': 'This is a question2',
      'answer': 'This is an answer2', 
      'difficulty': 2,
      'category': 5
    },
    {
      'id': 4,
      'question': 'This is a question3',
      'answer': 'This is an answer3', 
      'difficulty': 2,
      'category': 3
    },
  ],
  "total_books": 3,
  "success": true
}
```