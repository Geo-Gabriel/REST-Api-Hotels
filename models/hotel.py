from database.sql_alchemy import db, get_uuid


class HotelModel(db.Model):
    __tablename__ = 'hotels'

    hotel_id = db.Column(db.String(80), primary_key=True, default=get_uuid, nullable=False, unique=True)
    name = db.Column(db.String(80))
    stars = db.Column(db.Float(precision=1))
    daily = db.Column(db.Float(precision=2))
    location = db.Column(db.String(40))
    site_id = db.Column(db.String(), db.ForeignKey('sites.site_id'))

    def __init__(self, name, stars, daily, location, site_id) -> None:
        # self.hotel_id = hotel_id
        self.name = name
        self.stars = stars
        self.daily = daily
        self.location = location
        self.site_id = site_id

    # class method extended from db.Model()
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
             return hotel
        return None

    def update_hotel(self, name, stars, daily, location):
        self.name = name
        self.stars = stars
        self.daily = daily
        self.location = location

    def save(self):
        db.session.add(self)  # auto save object in db
        db.session.commit()

    def delete(self):
        db.session.delete(self)  # auto delete object in db
        db.session.commit()

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'stars': self.stars,
            'daily': self.daily,
            'location': self.location,
            'site_id': self.site_id
        }
