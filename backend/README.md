# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the backend folder;

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=True
flask run
```

### Endpoints

#### Base URL
```bash
http://localhost:5000
```

##### GET  '/categories' 
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs and a success message. 

*curl request:*
```bash
curl http://localhost:5000/categories
```
**Expected Response:**
```bash 
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
##### GET  '/questions'
- Fetches a dictionary of questions.
- Also fetches a dictionary of categories as formatted in `/category`.
- Request Arguments: page
- Returns: An object consisting of two keys which in turn are objects.

*curl request:* 
```bash
http://localhost:5000/questions
```
**Expected Response:**
```bash 
{
 "categories": {
   "1": "Science",
   "2": "Art",
   "3": "Geography",
   "4": "History",
   "5": "Entertainment",
   "6": "Sports"
 }, 
 "questions": [
  {
   "answer": "Apollo 13",
   "category": 5,
   "difficulty": 4,
   "id": 2,
   "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }, ...
 ],
 "success": true,
 "total_categories": 6,
 "total_questions": 24
}
```

*Adding arguments for pagination*

##### GET '/questions?page=1'

**There are only 3 pages present**

##### DELETE '/questions/<int:id>'
- Deletes a question by id.
- Request Arguments: None.

*curl request:*
```bash
curl -X DELETE http://localhost:5000/questions/3
```
**Expected Response:**
```bash 
{
 "deleted": 3,
 "questions": [
  {
   "answer": "Apollo 13",
   "category": 5,
   "difficulty": 4,
   "id": 2,
   "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }, ...
 ],
 "success": true,
 "total_questions": 23
}
```

##### POST  '/questions'
- Creates a new question object.
- Takes question, answer, category(between 1 - 6), and takes difficulty(between 1 - 5)
- Request Arguments: None.

*curl request:*
```bash
curl -X POST http://localhost:5000/questions -H 'Content-Type: application/json' -d '{"question": "What language is this?", "answer": "Python", "category": 1, "difficulty": 1}'
```

**Expected Response:**
```bash 
{
 "created_id": 30,
 "questions": [
  {
   "answer": "Apollo 13",
   "category": 5,
   "difficulty": 4,
   "id": 2,
   "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }, ...
 ],
 "success": true,
 "total_questions": 24
}
```

##### POST  '/questions/search'
- Searches for a question if the `searchTerm` matches any question.
- Request Arguments: None.
- Returns: An object of questions in which there is a match with the `searchTerm`

*curl request:*
```bash
curl -X POST http://localhost:5000/questions/search -H 'Content-Type: application/json' -d '{"searchTerm": "What"}'
```

**Expected Response:**
```bash 
{
 "questions": [
  {
   "answer": "Apollo 13",
   "category": 5,
   "difficulty": 4,
   "id": 2,
   "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }, ...
 ],
 "success": true,
 "total_questions": 9
}
```

##### GET  '/categories/<int:id>/questions'
- Fetches questions that match the category of `id`.
- Request Arguments: None.
- Returns an object of questions that match the category of `id`.

*curl request:*
```bash
curl http://localhost:5000/categories/1/questions
```

**Expected Response:**
```bash 
{
 "current_category": "Science",
 "questions": [
  {
   "answer": "The Liver",
   "category": 1,
   "difficulty": 4,
   "id": 20,
   "question": "What is the heaviest organ in the human body?"
  }, ...
 ],
 "success": true,
 "total_questions": 4
}
```

##### POST  '/quizzes'
- Fetches Categories first then posts an answer.

*curl request:*
```bash
curl -X POST http://localhost:5000/quizzes -H 'Content-Type: application/json' -d '{"previous_questions": [2, 5, 1], "quiz_category": {"type": "Science", "I'd": 1}}'
```

**Expected Response:**
```bash 
{
 "question": {
   "answer": "Blood",
   "category": 1,
   "difficulty": 4,
   "id": 22,
   "question": "Hematology is the branch of medicine involving the study of what?"
 },
 "success": true
}
```

## Error Response:
```bash 
{
  "error": 404,
  "message": "Not Found",
  "success": false
}
```

## Testing

To run the tests, run
```bash
dropdb trivia_test

createdb trivia_test

psql trivia_test < trivia.psql

python test_flaskr.py
```
