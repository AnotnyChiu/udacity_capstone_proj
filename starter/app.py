import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import CreateEntity
import sys


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # db setting
    app.config.from_object('config')
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # cors config
    CORS(app, resources={"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        return response

    # get models
    Movie, Actor, Director, MovieActor = CreateEntity(db)

    # region: movie endpoint
    @app.route('/movies')
    def get_movies():
        try:
            movies = [m.json_format() for m in Movie.query.all()]
            
            return jsonify({
                'success': True,
                'movies': movies
            })

        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(404)

    @app.route('/movies/<int:movie_id>')
    def get_movie_by_id(movie_id):
        try:
            movie = (Movie.query
                     .filter(Movie.id == movie_id)
                     .one_or_none())
            
            # print(movie.director.json_format())
            print([ma.ma_actor.name for ma in movie.movie_actor])

            if movie is None:
                abort(400)

            return jsonify({
                'success': True,
                'movie': movie.json_format()
            })

        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(500)

    @app.route('/movies', methods=['POST'])
    def add_movie():
        try:
            body = request.get_json()

            insert_movie = Movie(
                title=body.get('title', None),
                release_date=body.get('release_date', None),
                director_id=body.get('director_id', None)
            )

            insert_movie.insert()
            return jsonify({
                'suceess': True,
                'new_movie': insert_movie.id
            })

        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['PUT'])
    def update_movie(movie_id):
        try:
            body = request.get_json()
            movie = (Movie.query
                     .filter(Movie.id == movie_id)
                     .one_or_none())

            if movie is None:
                abort(422)
            
            movie.title = body.get('title', None)
            movie.release_date = body.get('release_date', None)
            movie.director_id = body.get('director_id', None)
            movie.update()

            return jsonify({
              'success': True,
              'updated_movie': movie.json_format()
            })
        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(400)
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        try:
            movie = (Movie.query
                     .filter(Movie.id == movie_id)
                     .one_or_none())
            
            if movie is None:
                abort(400)
            
            movie.delete()

            return jsonify({
                'success': True,
                'deleted_movie': movie_id
            })
        except:
            err_msg = sys.exc_info()
            print(err_msg)
            abort(422)
    # endregion

    # region: actor endpoints
    @app.route('/actors')
    def get_actors():
        try:
            actors = [a.json_format() for a in Actor.query.all()]

            if actors is None:
                abort(404)

            return jsonify({
                'success': True,
                'actors': actors
            })
        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(500)
    
    @app.route('/actors/<int:actor_id>')
    def get_actor_by_id(actor_id):
        try:
            actor = (Actor.query
                     .filter(Actor.id == actor_id)
                     .one_or_none)
            
            if actor is None:
                abort(400)
            
            return jsonify({
                'success': True,
                'actor': actor.json_format()
            })
        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(500)

    @app.route('/actors', methods=['POST'])
    def add_actor():
        try:
            body = request.get_json()
            new_actor = Actor(
                name = body.get('name', None),
                age = body.get('age', None),
                gender = body.get('gender', None)
            )

            new_actor.insert()

            return jsonify({
                'success': True,
                'new_actor': new_actor.id
            })

        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(400)
    
    @app.route('/actors/<int:actor_id>', methods=['PUT'])
    def update_actor(actor_id):
        try:
            body = request.get_json()
            actor = (Actor.query
                     .filter(Actor.id == actor_id)
                     .one_or_none)
            
            actor.name = body.get('name', None)
            actor.age = body.get('age', None)
            actor.gender = body.get('gender', None)

            actor.update()

            return jsonify({
                'success': True,
                'updated_actor': actor.json_format()
            })
        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = (Actor.query
                     .filter(Actor.id == actor_id)
                     .one_or_none)
            
            if actor is None:
                abort(400)
            
            actor.delete()

            return jsonify({
                'success': True,
                'deleted_actor': actor_id
            })
        except:
            err_msg = sys.exc_info()
            print(err_msg)
            abort(422)
    # endregion

    # region: director endpoints
    # endregion

    # region: movie_actor endpoints
    # endregion


    # region: error_handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    # endregion
    return app


APP = create_app()

if __name__ == '__main__':
    # remember to remove when publishing
    APP.env = 'development'
    APP.run(host='0.0.0.0', port=8080, debug=True)
