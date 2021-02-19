import logging

from flask import Blueprint, make_response, request, abort
from flask.json import jsonify
from werkzeug.datastructures import FileStorage

from sqlalchemy.orm.exc import NoResultFound

from metadata import json
from metadata.contexts import DatabaseContext
from metadata.models import Archive, Configuration

from pydas import constants
from pydas import scopes
from pydas.routes.utils import get_session, verify_scopes
from pydas.archive import download_archive, upload_archive

archives_bp = Blueprint('archives',
                        'pydas.routes.archives',
                        url_prefix='/api/v1/archives')


@archives_bp.route(constants.BASE_PATH, methods=[constants.HTTP_GET, constants.HTTP_POST])
def index():
    session = get_session()

    if request.method == constants.HTTP_GET:
        logging.info("Fetching archive metadata from sDAS database")
        archives = session.query(Archive).all()
        return jsonify([json(archive) for archive in archives])

    if len(request.files) > 0:
        # Handling file upload in IPFS
        logging.info("Handling archive file upload request")
        file: FileStorage = request.files['dataset']
        context = DatabaseContext('pydasadmin', 'root')
        connection_string = context.get_configuration(
            'archiveIpfsConnectionString')
        if connection_string is None:
            logging.error(
                "No connection string was found, unable to upload to IPFS!")
            abort(500)

        symbols = request.form['company_symbols']
        logging.info("Uploading archive")
        archive = upload_archive(file.stream.read(),
                                 connection_string.value,
                                 context,
                                 company_symbols=symbols)
    else:
        # Support registering existing dataset metadata within sDAS
        logging.info("Registering archive in sDAS metadata database")
        archive = Archive.from_meta(request.get_json())
        archive_count = session.query(Archive).filter(
            Archive.address == archive.address).count()
        if archive_count > 0:
            message = f'Found possible dataset duplicate at address "{archive.address}".'
            logging.warning(message)
            response = make_response(message, 400)
            return response

        session.add(archive)
        session.commit()

    return jsonify(json(archive))


@archives_bp.route('/<archive_address>', methods=[constants.HTTP_GET])
def archive_index(archive_address):
    session = get_session()
    try:
        archive = session.query(Archive).filter(
            Archive.address == archive_address).one()
        if archive is not None:
            return jsonify(json(archive))
    except NoResultFound:
        message = f'Cannot find requested archive with address "{archive_address}"'
        logging.error(message)
        response = make_response(message, 404)
        return response


@archives_bp.route('/<archive_address>/download', methods=[constants.HTTP_GET])
def archive_data(archive_address):
    session = get_session()
    connection_string = session.query(Configuration).filter(
        Configuration.name == 'archiveIpfsConnectionString').one_or_none()
    if connection_string is None:
        logging.error(
            "No connection string was found, unable to upload to IPFS!")
        abort(500)

    try:
        archive = session.query(Archive).filter(
            Archive.address == archive_address).one()
        return jsonify(download_archive(archive.address, connection_string.value))
    except NoResultFound:
        message = f'Cannot find requested archive with address "{archive_address}"'
        logging.error(message)
        response = make_response(message, 404)
        return response