from flask import Flask

# note: I think this should call the setup, but it doesn't... I'd need to
# call app.run()... hmmm.... I need to learn more about how Flask does this.
#from flask.ext.cqlengine import CQLEngine
# Not sure if a database script is supposed to have an app, and thus is
# privy to app's settings, like the connection info.
from cqlengine import connection
connection.setup(['127.0.0.1'])

from cqlengine.models import Model

from cqlengine.management import sync_table

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    model_attributes = [getattr(models, name) for name in dir(models)]
    entities = []
    for e in model_attributes:
        try:
            if issubclass(e, Model) and e != Model:
                entities.append(e)
        except:
            pass
    print entities
    #...and create your CQL table
    for e in entities:
        print 'creating table for {0}'.format(e)
        sync_table(e)

if __name__ == '__main__':
    init_db()

