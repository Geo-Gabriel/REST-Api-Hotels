from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [s.json() for s in SiteModel.query.all()]}


class Site(Resource):

    def get(self, site_url):
        site = SiteModel.find_site(site_url=site_url)
        if site:
            return site.json(), 200
        return {'message': 'Site not found.'}, 404

    def post(self, site_url):
        if SiteModel.find_site(site_url=site_url):
            return {'message': f"Site '{site_url}' already exists."}, 400

        new_site = SiteModel(site_url=site_url)
        try:
            new_site.save()
        except:
            return {"message": "An internal error ocurred trying to create a new site"}, 500
        return new_site.json(), 201
    
    def delete(self, site_url):
        site = SiteModel.find_site(site_url=site_url)
        if site:
            try:
                site.delete()
                return {'message': 'Site deleted'}, 200
            except:
                return {'message': 'Error while deleting site'}, 501
        return {'message': 'Site not found.'}, 401
