import logging

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, make_response, request, abort
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.datastructures import FileStorage

from pydas_auth import scopes
from pydas_auth import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Archive, Configuration

from pydas import constants
from pydas.archive import download_archive, upload_archive
from pydas.containers import ApplicationContainer

archives_bp = Blueprint('archives',
                        'pydas.routes.archives',
                        url_prefix='/api/v1/archives')


@archives_bp.route(constants.BASE_PATH, methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.ARCHIVES_READ,
                constants.HTTP_POST: scopes.ARCHIVES_WRITE},
               current_app,
               request)
@inject
def index(metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    if request.method == constants.HTTP_GET:
        logging.info("Fetching archive metadata from sDAS database")
        with metadata_context.get_session() as session:
            archives = session.query(Archive).all()
            return jsonify([json(archive) for archive in archives])

    if len(request.files) > 0:
        # Handling file upload in IPFS
        logging.info("Handling archive file upload request")
        file: FileStorage = request.files['dataset']
        connection_string = metadata_context.get_configuration(
            'archiveIpfsConnectionString')
        if connection_string is None:
            logging.error(
                "No connection string was found, unable to upload to IPFS!")
            abort(500)

        symbols = request.form['company_symbols']
        logging.info("Uploading archive")
        archive = upload_archive(file.stream.read(),
                                 connection_string.value,
                                 metadata_context,
                                 company_symbols=symbols)
    else:
        # Support registering existing dataset metadata within sDAS
        logging.info("Registering archive in sDAS metadata database")
        archive = Archive.from_meta(request.get_json())
        with metadata_context.get_session() as session:
            archive_count = session.query(Archive).filter(
                Archive.address == archive.address).count()
            if archive_count > 0:
                message = f'Found possible dataset duplicate at address "{archive.address}".'
                logging.warning(message)
                response = make_response(message, 400)
                return response

            session.add(archive)

    return jsonify(json(archive))


@archives_bp.route('/<archive_address>', methods=[constants.HTTP_GET])
@verify_scopes({constants.HTTP_GET: scopes.ARCHIVES_READ},
               current_app,
               request)
@inject
def archive_index(archive_address: str,
                  metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
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
@verify_scopes({constants.HTTP_GET: scopes.ARCHIVES_READ},
               current_app,
               request)
@inject
def archive_data(archive_address: str,
                 metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    with metadata_context.get_session() as session:
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
