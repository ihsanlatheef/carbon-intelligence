from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.region import Region


@app.route('/regions', methods=['GET'])
@db_session_wrap
def get_create_regions(session):
    if request.method == 'GET':
        query = session.query(
            Region
        ).order_by(
            Region.id
        )
        return jsonify([region.asdict() for region in query.all()])

    if request.method == 'POST':
        new = Region(**request.get_json())
        session.add(new)
        session.commit()
        return jsonify(new.asdict())


@app.route('/regions/<id>/', methods=['GET', 'PUT', 'DELETE'])
@db_session_wrap
def get_update_delete_region(session, id):
    region = session.query(Region).get(id)
    if not region:
        abort(404)

    if request.method == 'DELETE':
        session.delete(region)
        session.commit()
        return {'success': True}

    if request.method == 'PUT':
        for key, value in request.get_json().items():
            setattr(region, key, value)
        session.commit()

    return jsonify(region.asdict())
