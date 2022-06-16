# from crypt import methods
from json import load
import os
from unicodedata import category
from unittest import result
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.orm import load_only

from sqlalchemy import select

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [quest.format() for quest in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO[DONE]: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO[DONE]: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = db.session.query(Category).order_by(Category.id).all()
    
        return jsonify ({
            'success': True,
            'categories': {cat.id: cat.type for cat in categories}
        })
        

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        # selection = db.session.query(Question).order_by(Question.id)
        selection = db.session.query(Question).options(load_only(Question.question, Question.category)).order_by(Question.id)
        # selection = Question.query.with_entities(Question.question, Question.category)
        # selection = Question.query.options(load_only(Question.category)).all()
        # selection = db.session.query(Question.question, Question.category)
        categories = Category.query.all()
        question = Question.query.all()
        # return selection
        questions = paginate_questions(request, selection)
        return jsonify(
            {
                "success": True,
                "questions": list(questions),
                "total_questions": len(question),
                "total_categories": {cat.id: cat.type for cat in categories}
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            del_question = Question.query(Question.question).filter(Question.id == question_id)
            if question is None:
                abort(422)
            question.delete()
            selection = Question.query.order_by(question.id).all()
            current_questions = paginate_questions(request, selection)
            tot_question = len(Question.query.all())
        except:
            abort(422)
        finally:
            return jsonify({
                'success': True,
                'question_id': question_id,
                'question_deleted': del_question,
                'questions': current_questions,
                'total_questions': tot_question
            })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/question', methods=['POST'])
    def add_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer,
             category=new_category, difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            tot_questions = Question.query.all()

        except:
            abort(422)
        finally:
            return jsonify({
                'success': True,
                'created': question,
                'questions': current_questions,
                'total_questions': len(tot_questions)
            })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions?search=""')
    def search_questions(search):
        search = args.g

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

