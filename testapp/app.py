import os
import sys
import traceback

from flask import Flask, redirect, render_template, request, url_for
from flask.ext.cqlengine import CQLEngine

from datetime import datetime

import settings

# Initialize simple Flask application
app = Flask(__name__)
app.config.from_object(settings)

# This engages cqlengine so that the model works.
cqlengine = CQLEngine(app)


@app.route('/')
def home():
    """
    Create a row in Cassandra and show count of rows
    """
    from models import Foo
    Foo.create(kind=0, description='testcreate', created_at=datetime.now())
    return render_template('index.html', count=Foo.objects.count())

if __name__ == '__main__':
    app.run()
