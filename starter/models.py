# wrap models creation in functio and pass to app
from sqlalchemy.orm import backref


def CreateEntity(db):
    # basic model
    class Movie(db.Model):
        __tablename__ = 'movie'

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String)
        release_date = db.Column(db.Date)
        director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable=False)
        actors = db.relationship('Actor', secondary="movie_actor", viewonly=True)
        
        def __repr__(self):
            return f'<Movie_{self.id}: {self.title}>'
        
        def json_format(self):
            return {
                'id': self.id,
                'title': self.title,
                'release_date': self.release_date,
                'director': {
                    'id': self.director.id,
                    'name': self.director.name,
                    'age': self.director.age,
                    'gender': self.director.gender
                },
                'actors': [{
                    'id': ma.ma_actor.id,
                    'name':ma.ma_actor.name,
                    'age': ma.ma_actor.age,
                    'gender': ma.ma_actor.gender,
                    'pay': ma.actor_pay
                } for ma in self.movie_actor],
            }

        def __init__(self, title, release_date, director_id):
            self.title = title,
            self.release_date = release_date,
            self.director_id = director_id
        
        def insert(self):
            db.session.add(self)
            db.session.commit()
        
        def update(self):
            db.session.commit()
        
        def delete(self):
            db.session.delete(self)
            db.session.commit()


    class Actor(db.Model):
        __tablename__ = 'actor'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)
        age = db.Column(db.Integer)
        gender = db.Column(db.String)
        movies = db.relationship('Movie', secondary='movie_actor', viewonly=True)

        def __repr__(self):
            return f'<Actor_{self.id}: {self.name}>'
        
        def json_format(self):
            return {
                'id': self.id,
                'name': self.name,
                'age': self.age,
                'gender': self.gender,
                'movies': [{
                    'id': ma.ma_movie.id,
                    'title': ma.ma_movie.title,
                    'release_date': ma.ma_movie.release_date
                } for ma in self.movie_actor]
            }

        def __init__(self, name, age, gender):
            self.name = name,
            self.age = age
            self.gender = gender

        def insert(self):
            db.session.add(self)
            db.session.commit()
        
        def update(self):
            db.session.commit()
        
        def delete(self):
            db.session.delete(self)
            db.session.commit()


    class Director(db.Model):
        __tablename__ = 'director'

        id = db.Column(db.Integer,primary_key=True)
        name = db.Column(db.String)
        age = db.Column(db.Integer)
        gender = db.Column(db.String)
        movies = db.relationship('Movie', backref='director')

        def __repr__(self):
            return f'<Director_{self.id}: {self.name}>'
        
        def json_format(self):
            return {
                'id': self.id,
                'name': self.name,
                'age': self.age,
                'gender': self.gender,
                'movies': [{
                    'id': m.id,
                    'title': m.title,
                    'release_date': m.release_date
                } for m in self.movies]
            }
        
        def __init__(self, name, age, gender):
            self.name = name,
            self.age = age,
            self.gender = gender
        
        def insert(self):
            db.session.add(self)
            db.session.commit()
        
        def update(self):
            db.session.commit()
        
        def delete(self):
            db.session.delete(self)
            db.session.commit()
    

    # to perform many to many relationship,
    # need an "association table or association object" to cennect the two
    # here use an association object since this object contains not only 
    # the foreign keys of two tables but a third attribute "actor_pay"
    class MovieActor(db.Model):
        __tablename__ = 'movie_actor'

        id = db.Column(db.Integer, primary_key=True)
        actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
        movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
        actor_pay = db.Column(db.Integer)
        # back ref
        ma_actor = db.relationship('Actor', backref=backref('movie_actor', cascade='all, delete-orphan'))
        ma_movie = db.relationship('Movie', backref=backref('movie_actor', cascade='all, delete-orphan'))

        def __repr__(self):
            return (f'<MovieActor_{self.id}\n>'
            "Movie Name: {self.ma_movie.name} \n"
            "Actor Name: {self.ma_actor.name} \n"
            "Actor Pay: {self.actor_pay}"
            )
        
        def json_format(self):
            return{
                'id': self.id,
                'actor_id': self.actor_id,
                'movie_id': self.movie_id,
                'actor_pay': self.actor_pay
            }
        
        def __init__(self, actor_id, movie_id, actor_pay):
            self.actor_id = actor_id
            self.movie_id = movie_id
            self.actor_pay = actor_pay
        
        def insert(self):
            db.session.add(self)
            db.session.commit()
        
        def update(self):
            db.session.commit()
        
        def delete(self):
            db.session.delete(self)
            db.session.commit()


    return Movie, Actor, Director, MovieActor, db

'''

## relationship ##

1. A movie has several actors
2. An actor participates several movies
>> Many to Many relation

3. A movie has one director
4. A director has directed several movies
>> One to many relation

'''

'''
Once finished the modeling
1. setup your db in postgres
2. run the migration and let it create tables for you (no need db.create_all())

# commands:
1. flask db init (to create the migration folders)
2. flask db migrate (to create the migration file)
3. flask db upgrade (create or alter tables in postgres)
'''