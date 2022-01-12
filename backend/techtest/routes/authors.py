from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.author import Author


@app.route('/authors', methods=['GET', 'POST'])
@db_session_wrap
def get_create_authors(session):
    if request.method == 'GET':
        query = session.query(
            Author
        ).order_by(
            Author.id
        )
        return jsonify([author.asdict() for author in query.all()])

    if request.method == 'POST':
        new = Author(**request.get_json())
        session.add(new)
        session.commit()
        return jsonify(new.asdict())


@app.route('/authors/<id>/', methods=['GET', 'PUT', 'DELETE'])
@db_session_wrap
def get_update_delete_author(session, id):
    author = session.query(Author).get(id)
    if not author:
        abort(404)

    if request.method == 'DELETE':
        session.delete(author)
        session.commit()
        return {'success': True}

    if request.method == 'PUT':
        for key, value in request.get_json().items():
            setattr(author, key, value)
        session.commit()

    return jsonify(author.asdict())
