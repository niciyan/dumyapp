from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, index=True)
    message = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=10):
        from random import seed, randint, choice
        
        seed()
        user_count = User.query.count()
        SAMPLE_MESSAGES = [
                "いいんじゃない？",
                "おｋ",
                "こんにちは",
                "おつかれさん",
                "ただいま",
                "会議中",
                "continueed",
                "Hello!",
                "元気げんき",
                ]
        for i in range(count):
            u = User.query.offset(randint(0, user_count -1)).first()
            m = Message(message=choice(SAMPLE_MESSAGES),date=datetime.utcnow(), author=u)
            db.session.add(m)
            db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Message', backref='author', lazy='dynamic')
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
