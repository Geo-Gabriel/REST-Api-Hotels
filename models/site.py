from database.sql_alchemy import db, get_uuid


class SiteModel(db.Model):
    __tablename__ = 'sites'

    site_id = db.Column(db.String(80), primary_key=True, default=get_uuid, unique=True, nullable=False)
    site_url = db.Column(db.String(100))
    hotels = db.relationship('HotelModel')  # hotels list

    def __init__(self, site_url) -> None:
        self.site_url = site_url

    # class method extended from db.Model()
    @classmethod
    def find_site(cls, site_url):
        site = cls.query.filter_by(site_url=site_url).first()
        if site:
             return site
        return None

    @classmethod
    def find_site_by_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site
        return None

    def update_site(self, site_url):
        self.site_url = site_url

    def save(self):
        db.session.add(self)  # auto save object in db
        db.session.commit()

    def delete(self):
        # deleting all hotels from the site
        for hotel in self.hotels:
            hotel.delete()

        db.session.delete(self)  # auto delete object in db
        db.session.commit()

    def json(self):
        return {
            'site_id': self.site_id,
            'site_url': self.site_url,
            'hotels': [h.json() for h in self.hotels]
        }
