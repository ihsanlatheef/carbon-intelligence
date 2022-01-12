from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.article import Article


@app.route('/articles', methods=['GET', 'POST'])
@db_session_wrap
def get_create_articles(session):
    if request.method == 'GET':
        query = session.query(
            Article
        ).order_by(
            Article.id
        )
        return jsonify([
            article.asdict(follow=['regions', 'author']) for article in query.all()
        ])

    if request.method == 'POST':
        new = Article(**request.get_json())
        session.add(new)
        session.commit()
        return jsonify(new.asdict(follow=['regions', 'author']))


@app.route('/articles/<id>/', methods=['GET', 'PUT', 'DELETE'])
@db_session_wrap
def get_update_delete_article(session, id):
    article = session.query(Article).get(id)
    if not article:
        abort(404)

    if request.method == 'DELETE':
        session.delete(article)
        session.commit()
        return {'success': True}

    if request.method == 'PUT':
        for key, value in request.get_json().items():
            setattr(article, key, value)
        session.commit()

    return jsonify(article.asdict(follow=['regions', 'author']))
