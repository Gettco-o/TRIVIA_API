import os
from signal import Handlers
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # AFter request

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response


    # Get Categories

    @app.route("/categories")
    def list_categories():
        selection = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in selection]

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": {category.id: category.type for category in selection}
            }
        )


    # Paginate questions

    def paginate_questions(request, que_selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in que_selection]
        current_questions = questions[start:end]

        return current_questions


    # Get Questions

    @app.route("/questions")
    def get_questions():
        que_selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, que_selection)

        categories = Category.query.order_by(Category.id).all()

        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(que_selection),
            'categories': {category.id: category.type for category in categories},
            'currentCategory': "All"
        })


    # Delete Question

    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id==question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)


   # Create a Question
    
    @app.route("/questions", methods=['POST'])
    def submit_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer, 
            difficulty=new_difficulty, category=new_category)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })

        except:
            abort(422)


    #Search for questions with a keyword
        
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm', None)

        try:
            if search:
                questions = Question.query.order_by(Question.id).filter(
                        Question.question.ilike("%{}%".format(search))
                    )
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': len(questions.all()),
                    'currentCategory': "All"
                })
        except:
            abort(404)



    # Get questions by category 

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        category = Category.query.filter(Category.id==category_id).one_or_none()

        try:
            questions = Question.query.filter(Question.category==category_id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'totalQuestions': len(questions),
                'currentCategory': category.type
            })
        except:
            abort(404)



    # Get questions to play quiz

    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        try:
            body = request.get_json()

            category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            if category['type'] == 'all':
                available_questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
            else:
                available_questions = Question.query.filter_by(category=category['id']).filter(Question.id.notin_((previous_questions))).all()

            new_question = available_questions[random.randrange(0, 
            len(available_questions))].format() if len(available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)



    # Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    

    return app

