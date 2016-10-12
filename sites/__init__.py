from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
import pymongo

from sites.resources import Root

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
    config.add_view('sites.views.my_view',
                    context='sites:resources.Root',
                    renderer='sites:templates/mytemplate.pt')
    config.add_static_view('static', 'sites:static')
    config.include('pyramid_chameleon')
    # MongoDB
    def add_mongo_db(event):
        settings = event.request.registry.settings
        url = settings['mongodb.url']
        db_name = settings['mongodb.db_name']
        db = settings['mongodb_conn'][db_name]
        event.request.db = db
    db_uri = settings['mongodb.url']
    MongoDB = pymongo.MongoClient
    if 'pyramid_debugtoolbar' in set(settings.values()):
        class MongoDB(pymongo.MongoClient):
            def __html__(self):
                return 'MongoDB: <b>{}></b>'.format(self)
    conn = MongoDB(db_uri)
    config.registry.settings['mongodb_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)
    config.scan('.views')
    return config.make_wsgi_app()
