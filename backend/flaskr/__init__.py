import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={"/": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
      response.headers.add("Access-Control-Allow-Methods", ["GET", "POST", "PATCH", "DELETE", "OPTIONS"])
      return response

#ROUTES

  #Get all categories
  @app.route('/categories')
  def get_categories():
      data = Category.query.all()
      categories = {}

      if data is None:
          abort(404)

      for category in data:
          categories[category.id] = category.type

      return jsonify({
          "success": True,
          "categories": categories
          })

  #Get all questions
  @app.route('/questions')
  def get_questions():
      selection = Question.query.order_by(Question.id).all()
      data = Category.query.all()
      categories = {}

      current_questions = paginate_questions(request, selection)

      if not len(current_questions):
          abort(404)

      for category in data:
          categories[category.id] = category.type

      return jsonify({
          "success": True,
          "questions": current_questions,
          "total_questions": len(selection),
          "categories": categories,
          "total_categories": len(data)
          })

  #Delete
  @app.route("/questions/<int:id>", methods=["DELETE"])
  def delete_question(id):
      try:
          question = Question.query.filter(Question.id == id).one_or_none()

          if question is None:
              abort(404)

          question.delete()

          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)

          return jsonify({
              "success": True,
              "deleted": question.id,
              "questions": current_questions,
              "total_questions": len(selection)
              })

      except:
          abort(422)

  #create a new question
  @app.route('/questions', methods=['POST'])
  def create_question():
      body = request.get_json()

      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)

      try:
          question = Question(
                  question = new_question,
                  answer = new_answer,
                  category = new_category,
                  difficulty = new_difficulty
                  )
          question.insert()

          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)

          return jsonify({
              "success": True,
              "created_id": question.id,
              "questions": current_questions,
              "total_questions": len(selection)
              })

      except:
          abort(422)

  #search
  @app.route('/questions/search', methods=['POST'])
  def search_question():
      search = request.get_json()

      if(search['searchTerm']):
          search_term = search['searchTerm']

      selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

      if not len(selection):
          abort(404)

      questions = paginate_questions(request, selection)

      return jsonify({
          "success": True,
          "questions": questions,
          "total_questions": len(selection)
          })

  #get questions by category
  @app.route('/categories/<int:id>/questions')
  def render_questions(id):
      category = Category.query.filter_by(id=id).one_or_none()

      if category is None:
          abort(404)

      selection = Question.query.filter(Question.category == id).order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
          "success": True,
          "questions": current_questions,
          "total_questions": len(current_questions),
          "current_category": category.type
          })

  #play quiz
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
      body = request.get_json()

      previous_questions = body.get("previous_questions", None)
      quiz_category = body.get("quiz_category", None)
      cat_id = quiz_category['id']
      try:
          if (cat_id == 0):
              questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

          else:
              questions = Question.query.filter(Question.id.notin_(previous_questions)).filter(Question.category == cat_id).all()

          if (questions):
              question = random.choice(questions).format()

          return jsonify({
              "success": True,
              "question": question
              })

      except:
          abort(422)

  #error handling
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
          }), 400

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
          }), 500

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Not Found"
          }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
          }), 422

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method not allowed"
          }), 405

  return app

    
