import inspect
import urlparse

from cqlengine.connection import setup
from cqlengine_session import get_session, save
from werkzeug.utils import import_string

__all__ = ('CQLEngine', )


__version__ = '0.1'


class CQLEngine(object):
    """CQLEngine database support for Flask."""
    def __init__(self, app=None):
        """
        If app argument provided then initialize cqlengine connection using
        application config values.

        If no app argument provided you should do initialization later with
        :meth:`init_app` method.

        :param app: Flask application instance.

        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Read cqlengine settings from app configuration,
        initialize cqlengine connection and copy all public connection
        methods to current instance.

        :param app: Flask application instance.

        """
        # Put cqlengine to application extensions
        if not 'cqlengine' in app.extensions:
            app.extensions['cqlengine'] = {}

        # Initialize connection and store it to extensions
        hosts = app.config['CQLENGINE_HOSTS']
        default_keyspace = app.config['CQLENGINE_DEFAULT_KEYSPACE']

        # Configure cqlengine's global connection pool.
        setup(hosts, default_keyspace=default_keyspace)

        # We want to close the connection pool when the application closes.
        @app.teardown_appcontext
        def close_connection_pool(exception):
            from cqlengine.connection import connection_pool
            print connection_pool
            #connection_pool.clear()

        @app.before_request
        def clear_session():
            get_session(clear=True)

        @app.after_request
        def save_session(response):
            save()
            return response


    def _include_public_methods(self, connection):
        """
        Include public methods from connection instance to current instance.
        """
        for attr in dir(connection):
            value = getattr(connection, attr)
            if attr.startswith('_') or not callable(value):
                continue
            self.__dict__[attr] = value
