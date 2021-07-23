from database.sql_alchemy import db, get_uuid


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(80), primary_key=True, default=get_uuid, unique=True, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    # class method extended from db.Model()
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
             return user
        return None

    @classmethod
    def find_user_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
             return user
        return None

    def save(self):
        db.session.add(self)  # auto save object in db
        db.session.commit()

    def delete(self):
        db.session.delete(self) # auto delete object in db
        db.session.commit()

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username
            # "password": self.password 
        }
