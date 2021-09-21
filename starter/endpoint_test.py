from flask_sqlalchemy import SQLAlchemy
from werkzeug.http import parse_accept_header
from app import create_app
import unittest
import json
import copy

from app import create_app
from config import DB_NAME_TEST, DB_PATH_TEST

class CapstoneTestCase(unittest.TestCase):
    # setup
    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        # fake data for post test
        self.new_movie = {
            "title": "test_movie",
            "release_date": "2021-09-21",
            "director_id": 1
        }
        self.new_actor = {
            "name": "test_actor",
            "age": 22,
            "gender": "male"
        }
        self.new_director = {
            "name": "test_director",
            "age": 30,
            "gender": "female"
        }
        self.new_movie_actor = {
            "movie_id": 1,
            "actor_id": 1,
            "actor_pay": 10000
        }
    
    def tearDown(self) -> None:
        pass

    # test cases (post >> get >> put >> delete)
    # region: post
    def test_add_movie(self):
        res = self.client().post('/movies',json=self.new_movie)
        data = json.loads(res.data)

        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['new_movie'])
    
    def test_400_badrequest_on_movie_creation(self):
        mock = copy.copy(self.new_movie)
        mock["release_date"] = 'error format'
        res = self.client().post('/movies',json=mock)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "bad request")

    def test_add_actor(self):
        res = self.client().post('/actors',json=self.new_actor)
        data = json.loads(res.data)

        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['new_actor'])

    def test_400_on_actor_creation(self):
        mock = copy.copy(self.new_actor)
        mock["age"] = 'error format'
        res = self.client().post('/actors',json=mock)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "bad request")
    
    def test_add_director(self):
        res = self.client().post('/directors',json=self.new_director)
        data = json.loads(res.data)

        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['new_director'])

    def test_400_on_director_creation(self):
        mock = copy.copy(self.new_director)
        mock["age"] = 'error format'
        res = self.client().post('/directors',json=mock)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "bad request")
    
    def test_add_movie_actor(self):
        res = self.client().post('/movie_actors',json=self.new_movie_actor)
        data = json.loads(res.data)

        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['new_movie_actor'])

    def test_400_on_movie_actor_creation(self):
        mock = copy.copy(self.new_movie_actor)
        mock["actor_pay"] = 'error format'
        res = self.client().post('/movie_actors',json=mock)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "bad request")

    # endregion

    # region: get
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])
    
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def test_get_directors(self):
        res = self.client().get('/directors')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['directors'])

    def test_get_movie_actors(self):
        res = self.client().get('/movie_actors')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movie_actors'])

    def test_404_movies_actors_directors_movieactors_not_found(self):
        res = self.client().get('/wrong_url')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    
    def test_get_movie_by_id(self):
        # get the movie created
        get_movies_res = self.client().get('/movies')
        target_id = json.loads(get_movies_res.data)['movies'][-1]['id']
        # test
        res = self.client().get(f'/movies/{target_id}')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movie'])
    
    def test_400_get_movie_beyond_range(self):
        res = self.client().get('/movies/1000000000')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    def test_get_actor_by_id(self):
        # get the actor created
        get_actors_res = self.client().get('/actors')
        target_id = json.loads(get_actors_res.data)['actors'][-1]['id']
        # test
        res = self.client().get(f'/actors/{target_id}')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actor'])
    
    def test_400_get_actor_beyond_range(self):
        res = self.client().get('/actors/1000000000')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")
    
    def test_get_director_by_id(self):
        # get the director created
        get_directors_res = self.client().get('/directors')
        target_id = json.loads(get_directors_res.data)['directors'][-1]['id']
        # test
        res = self.client().get(f'/directors/{target_id}')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['director'])
    
    def test_400_get_director_beyond_range(self):
        res = self.client().get('/directors/1000000000')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")
    

    # endregion

    # region: put
    def test_update_movie(self):
        # get the movie created
        get_movies_res = self.client().get('/movies')
        target_id = json.loads(get_movies_res.data)['movies'][-1]['id']
        # test
        res = self.client().put(f'/movies/{target_id}', json=self.new_movie)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie'])

    def test_400_update_movie_with_wrong_format(self):
        # get the movie created
        get_movies_res = self.client().get('/movies')
        target_id = json.loads(get_movies_res.data)['movies'][-1]['id']
        # test
        mock = copy.copy(self.new_movie)
        mock['release_date'] = 'wrong_format'
        res = self.client().put(f'/movies/{target_id}', json=mock)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')
    
    def test_400_update_movie_with_invalid_id(self):
        res = self.client().put('/movies/100000000', json=self.new_movie)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')
    
    def test_update_actor(self):
        # get the actor created
        get_actors_res = self.client().get('/actors')
        target_id = json.loads(get_actors_res.data)['actors'][-1]['id']
        # test
        res = self.client().put(f'/actors/{target_id}', json=self.new_actor)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_actor'])

    def test_400_update_actor_with_wrong_format(self):
        # get the actor created
        get_actors_res = self.client().get('/actors')
        target_id = json.loads(get_actors_res.data)['actors'][-1]['id']
        # test
        mock = copy.copy(self.new_actor)
        mock['age'] = 'wrong_format'
        res = self.client().put(f'/actors/{target_id}', json=mock)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')
    
    def test_400_update_actor_with_invalid_id(self):
        res = self.client().put('/actors/100000000', json=self.new_actor)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')
    
    def test_update_director(self):
        # get the director created
        get_directors_res = self.client().get('/directors')
        target_id = json.loads(get_directors_res.data)['directors'][-1]['id']
        # test
        res = self.client().put(f'/directors/{target_id}', json=self.new_director)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_director'])

    def test_400_update_director_with_wrong_format(self):
        # get the director created
        get_directors_res = self.client().get('/directors')
        target_id = json.loads(get_directors_res.data)['directors'][-1]['id']
        # test
        mock = copy.copy(self.new_director)
        mock['age'] = 'wrong_format'
        res = self.client().put(f'/directors/{target_id}', json=mock)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')
    
    def test_400_update_director_with_invalid_id(self):
        res = self.client().put('/directors/100000000', json=self.new_director)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    def test_update_movie_actor(self):
        # get the movie_actor created
        get_movie_actors_res = self.client().get('/movie_actors')
        target_id = json.loads(get_movie_actors_res.data)['movie_actors'][-1]['id']
        # test
        res = self.client().put(f'/movie_actors/{target_id}', json=self.new_movie_actor)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie_actor'])

    def test_400_update_movie_actor_with_wrong_format(self):
        # get the movie_actor created
        get_movie_actors_res = self.client().get('/movie_actors')
        target_id = json.loads(get_movie_actors_res.data)['movie_actors'][-1]['id']
        # test
        mock = copy.copy(self.new_movie_actor)
        mock['actor_pay'] = 'wrong_format'
        res = self.client().put(f'/movie_actors/{target_id}', json=mock)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')
    
    def test_400_update_movie_actor_with_invalid_id(self):
        res = self.client().put('/movie_actors/100000000', json=self.new_movie_actor)
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    # endregion

    # region: delete
    def test_delete_movie(self):
        # get the movie created
        get_movies_res = self.client().get('/movies')
        target_id = json.loads(get_movies_res.data)['movies'][-1]['id']
        # test
        res = self.client().delete(f'/movies/{target_id}')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie'], target_id)

    def test_400_delete_movie_with_invalid_id(self):
        res = self.client().delete('/movies/100000000')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')
    
    def test_delete_actor(self):
        # get the actor created
        get_actors_res = self.client().get('/actors')
        target_id = json.loads(get_actors_res.data)['actors'][-1]['id']
        # test
        res = self.client().delete(f'/actors/{target_id}')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor'], target_id)

    def test_400_delete_actor_with_invalid_id(self):
        res = self.client().delete('/actors/100000000')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    def test_delete_director(self):
        # get the director created
        get_directors_res = self.client().get('/directors')
        target_id = json.loads(get_directors_res.data)['directors'][-1]['id']
        # test
        res = self.client().delete(f'/directors/{target_id}')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_director'], target_id)

    def test_400_delete_director_with_invalid_id(self):
        res = self.client().delete('/directors/100000000')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')
    
    def test_delete_movie_actor(self):
        # get the movie_actor created
        get_movie_actors_res = self.client().get('/movie_actors')
        target_id = json.loads(get_movie_actors_res.data)['movie_actors'][-1]['id']
        # test
        res = self.client().delete(f'/movie_actors/{target_id}')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie_actor'], target_id)

    def test_400_delete_movie_actor_with_invalid_id(self):
        res = self.client().delete('/movie_actors/100000000')
        data = json.loads(res.data)
        # assertion
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    # endregion
if __name__ == '__main__':
    unittest.main()