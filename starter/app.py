import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
from models import CreateEntity
from config import DB_PATH_TEST
import sys


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # db setting
    app.config.from_object('config')
    if test_config is True:
        app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH_TEST

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

            if movie is None:
                raise BadRequest

            return jsonify({
                'success': True,
                'movie': movie.json_format()
            })

        except BadRequest:
            abort(400)
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
                'success': True,
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
                raise BadRequest
            
            movie.title = body.get('title', None)
            movie.release_date = body.get('release_date', None)
            movie.director_id = body.get('director_id', None)
            movie.update()

            return jsonify({
              'success': True,
              'updated_movie': movie.json_format()
            })
        except BadRequest:
            abort(400)
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
                raise BadRequest
            
            movie.delete()

            return jsonify({
                'success': True,
                'deleted_movie': movie_id
            })
        except BadRequest:
            abort(400)
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

            return jsonify({
                'success': True,
                'actors': actors
            })
        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(404)
    
    @app.route('/actors/<int:actor_id>')
    def get_actor_by_id(actor_id):
        try:
            actor = (Actor.query
                     .filter(Actor.id == actor_id)
                     .one_or_none())
            
            if actor is None:
                raise BadRequest
            
            return jsonify({
                'success': True,
                'actor': actor.json_format()
            })
        
        except BadRequest:
            abort(400)
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
                     .one_or_none())
            
            if actor is None:
                raise BadRequest

            actor.name = body.get('name', None)
            actor.age = body.get('age', None)
            actor.gender = body.get('gender', None)

            actor.update()

            return jsonify({
                'success': True,
                'updated_actor': actor.json_format()
            })
        except BadRequest:
            abort(400)
        except:
            err_msg = sys.exc_info()
            print(err_msg)
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = (Actor.query
                     .filter(Actor.id == actor_id)
                     .one_or_none())
            
            if actor is None:
                raise BadRequest
            
            actor.delete()

            return jsonify({
                'success': True,
                'deleted_actor': actor_id
            })
        except BadRequest:
            abort(400)
        except:
            err_msg = sys.exc_info()
            print(err_msg)
            abort(422)
    # endregion

    # region: director endpoints
    @app.route('/directors')
    def get_directors():
        try:
            directors = [d.json_format() for d in Director.query.all()]

            return jsonify({
                'success': True,
                'directors': directors
            })
        except:
           error_msg = sys.exc_info()
           print(error_msg)
           abort(404)

    @app.route('/directors/<int:director_id>')
    def get_director_by_id(director_id):
        try:
            director = (Director.query
                        .filter(Director.id == director_id)
                        .one_or_none())
            
            if director is None:
                raise BadRequest
            
            return jsonify({
                'success': True,
                'director': director.json_format()
            })
        except BadRequest:
            abort(400)
        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(400)
    
    @app.route('/directors', methods=['POST'])
    def add_director():
        try:
            body = request.get_json()

            insert_director = Director(
                name = body.get('name', None),
                age = body.get('age', None),
                gender = body.get('gender', None)
            )

            insert_director.insert()
            return jsonify({
                'success': True,
                'new_director': insert_director.id
            })

        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(400)

    @app.route('/directors/<int:director_id>', methods=['PUT'])
    def update_director(director_id):
        try:
            body = request.get_json()
            director = (Director.query
                     .filter(Director.id == director_id)
                     .one_or_none())
            
            if director is None:
                raise BadRequest

            director.name = body.get('name', None)
            director.age = body.get('age', None)
            director.gender = body.get('gender', None)

            director.update()

            return jsonify({
                'success': True,
                'updated_director': director.json_format()
            })
        except BadRequest:
            abort(400)
        except:
            err_msg = sys.exc_info()
            print(err_msg)
            abort(400)

    @app.route('/directors/<int:director_id>', methods=['DELETE'])
    def delete_director(director_id):
        try:
            director = (Director.query
                     .filter(Director.id == director_id)
                     .one_or_none())
            
            if director is None:
                raise BadRequest
            
            director.delete()

            return jsonify({
                'success': True,
                'deleted_director': director_id
            })
        except BadRequest:
            abort(400)
        except:
            err_msg = sys.exc_info()
            print(err_msg)
            abort(422)
    # endregion

    # region: movie_actor endpoints
    @app.route('/movie_actors')
    def get_movie_actors():
        try:
            ma = [ma.json_format() for ma in MovieActor.query.all()]
            
            return jsonify({
                'success': True,
                'movie_actors': ma
            })

        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(404)
    
    @app.route('/movie_actors', methods=['POST'])
    def add_movie_actor():
        try:
            body = request.get_json()

            insert_ma = MovieActor(
                actor_id = body.get('actor_id', None),
                movie_id = body.get('movie_id', None),
                actor_pay = body.get('actor_pay', None)
            )

            insert_ma.insert()
            return jsonify({
                'success': True,
                'new_movie_actor': insert_ma.id
            })

        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(400)
    
    @app.route('/movie_actors/<int:ma_id>', methods=['PUT'])
    def update_movie_actor(ma_id):
        try:
            body = request.get_json()
            ma = (MovieActor.query
                     .filter(MovieActor.id == ma_id)
                     .one_or_none())

            if ma is None:
                raise BadRequest
            
            ma.actor_id = body.get('actor_id', None),
            ma.movie_id = body.get('movie_id', None),
            ma.actor_pay = body.get('actor_pay', None)
            ma.update()

            return jsonify({
              'success': True,
              'updated_movie_actor': ma.json_format()
            })
        except BadRequest:
            abort(400)
        except:
            error_msg = sys.exc_info()
            print(error_msg)
            abort(400)
    
    @app.route('/movie_actors/<int:ma_id>', methods=['DELETE'])
    def delete_movie_actor(ma_id):
        try:
            body = request.get_json()
            ma = (MovieActor.query
                     .filter(MovieActor.id == ma_id)
                     .one_or_none())

            if ma is None:
                raise BadRequest
            
            ma.delete()

            return jsonify({
                'success': True,
                'deleted_movie_actor': ma_id
            })
        except BadRequest:
            abort(400)
        except:
            err_msg = sys.exc_info()
            print(err_msg)
            abort(422)

    # endregion

    # region: error_handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400
    
    @app.errorhandler(401)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'forbidden'
        }),401

    @app.errorhandler(403)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'unauthorized'
        }),403

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
