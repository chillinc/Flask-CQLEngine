import unittest
import uuid

from cqlengine import columns
from cqlengine.management import create_keyspace, delete_keyspace, sync_table
from cqlengine.models import Model
from cqlengine_session import SessionModel
import flask
from flask.ext import cqlengine


def make_todo_model():
    class Todo(SessionModel):
        uuid = columns.UUID(primary_key=True, default=uuid.uuid4)
        title = columns.Text(max_length=60)
        text = columns.Text()
        done = columns.Boolean()
        pub_date = columns.DateTime()

    return Todo


class BasicAppTestCase(unittest.TestCase):

    def setUp(self):
        app = flask.Flask(__name__)
        app.config['TESTING'] = True
        app.config['CQLENGINE_HOSTS'] = 'localhost'
        app.config['CQLENGINE_PORT'] = '9042'
        app.config['CQLENGINE_DEFAULT_KEYSPACE'] = 'testkeyspace{}'.format(str(uuid.uuid1()).replace('-', ''))
        cqlengine.CQLEngine(app)
        self.Todo = make_todo_model()

        @app.route('/')
        def index():
            return '\n'.join(x.title for x in self.Todo.objects)

        @app.route('/add', methods=['POST'])
        def add():
            form = flask.request.form
            todo = self.Todo.create(title=form['title'], text=form['text'])
            return 'added'

        create_keyspace(app.config['CQLENGINE_DEFAULT_KEYSPACE'])
        self.Todo.sync_table()

        self.app = app

    def tearDown(self):
        delete_keyspace(self.app.config['CQLENGINE_DEFAULT_KEYSPACE'])

    def test_basic_insert(self):
        c = self.app.test_client()
        c.post('/add', data=dict(title='First Item', text='The text'))
        c.post('/add', data=dict(title='2nd Item', text='The text'))
        rv = c.get('/')
        self.assertTrue(rv.data == b'First Item\n2nd Item' or rv.data == b'2nd Item\nFirst Item')
