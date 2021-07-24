import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from werkzeug.exceptions import MethodNotAllowed, NotFound, UnprocessableEntity

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
    app = Flask(__name__, instance_relative_config=True)
    if test_config is not None:
        setup_db(app, test_config)
    else:
        setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTION')
        return response

    @app.route("/categories", methods=['GET'])
    def retrieve_categories():
        try:
            if request.method != 'GET':
                abort(405)       

            categories = Category.query.order_by(Category.id).all()

            result = {}
            for cat in categories:
                result[cat.id] = cat.type

            return jsonify({
                'success': True,
                'categories': result
            })
        except MethodNotAllowed:
            abort(405)

        except Exception:
            abort(500)

    @app.route("/questions", methods=['GET'])
    def retrieve_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            if len(current_questions) == 0:
                abort(404)

            categories = Category.query.order_by(Category.id).all()
            cat_formatted = {}
            for cat in categories:
                cat_formatted[cat.id] = cat.type

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': cat_formatted,
                'current_category': current_questions[0]['category']
            })
        except NotFound:
            abort(404)

        except Exception:
            abort(500)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(422)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            search = body.get('searchTerm', None)

            if search is None:
                abort(422)

            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search))).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': current_questions[0]['category']
            })

        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if (new_question is None or new_answer is None or
                new_category is None or new_difficulty is None):
            abort(422)

        try:
            question = Question(question=new_question,
                                answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty)
            question.insert()
            return jsonify({
                'success': True
            }), 201

        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        try:
            selection = Question.query.order_by(Question.id).filter(
                Question.category == category_id).all()

            if len(selection) == 0:
                abort(422)

            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category_id
            })

        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.route('/quizzes', methods=['POST'])
    def retrieve_next_quizz():
        try:
            body = request.get_json()

            prev_quizz_ids = body.get('previous_questions', None)
            category = body.get('quiz_category', None)

            if (prev_quizz_ids is None or category is None):
                abort(422)

            data = Question.query.filter(
                Question.category == int(category['id'])).filter(
                Question.id.notin_(prev_quizz_ids)).first()

            return jsonify({
                'success': True,
                'question': data.format() if data else None
            })

        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.errorhandler(400)
    def bad_request(self):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(self):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(self):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(self):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(self):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
