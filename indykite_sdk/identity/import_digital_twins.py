import sys
from indykite_sdk.indykite.identity.v1beta2 import import_pb2
from indykite_sdk.model.digital_twin_kind import DigitalTwinKind
from indykite_sdk.model.digital_twin_state import DigitalTwinState
import indykite_sdk.utils.logger as logger


def import_digital_twins(self, entities, hash_algorithm):
    """
    import digital twins
    :param self:
    :param entities: list of ImportDigitalTwin objects
    :param hash_algorithm: dict
    :return: list of ImportDigitalTwinsResponse
    """
    sys.excepthook = logger.handle_excepthook
    try:
        n = 1000
        response = []
        stub = self.stub
        chunks = list(divide_chunks(entities, n))
        for chunk in chunks:
            res = import_digital_twins_chunks(stub, chunk, hash_algorithm)
            if not res:
                return None
            response.append(res)

    except Exception as exception:
        return logger.logger_error(exception)

    return response


def import_digital_twins_chunks(stub, entities, hash_algorithm):
    """
    import chunk of digital twins
    :param stub:
    :param entities: list of ImportDigitalTwin objects
    :param hash_algorithm: dict
    :return: ImportDigitalTwinsResponse
    """
    try:
        idt = []
        for e in entities:
            if not validate_entity(e):
                return None
            idt.append(e)

        if hash_algorithm is None:
            data_request = import_pb2.ImportDigitalTwinsRequest(
                entities=idt
            )
        else:
            data_request = get_hash_request(idt, hash_algorithm)

        if data_request is None:
            return None
        response = stub.ImportDigitalTwins(
            data_request
        )
    except Exception as exception:
        return logger.logger_error(exception)

    if not response:
        return None

    return response


def get_hash_request(entities, hash_algorithm):
    """
    get entities with hash
    :param entities: list of ImportDigitalTwin objects
    :param hash_algorithm: dict
    :return: import_pb2.ImportDigitalTwinsRequest
    """
    try:
        hash_request = None
        for key in hash_algorithm:
            if key == 'bcrypt':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    bcrypt=hash_algorithm[key]
                )
            elif key == 'standard_scrypt':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    standard_scrypt=hash_algorithm[key]
                )
            elif key == 'scrypt':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    scrypt=hash_algorithm[key]
                )
            elif key == 'hmac_md5':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    hmac_md5=hash_algorithm[key]
                )
            elif key == 'hmac_sha1':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    hmac_sha1=hash_algorithm[key]
                )
            elif key == 'hmac_sha512':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    hmac_sha512=hash_algorithm[key]
                )
            elif key == 'hmac_sha256':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    hmac_sha256=hash_algorithm[key]
                )
            elif key == 'md5':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    md5=hash_algorithm[key]
                )
            elif key == 'pbkdf2_sha256':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    pbkdf2_sha256=hash_algorithm[key]
                )
            elif key == 'pbkdf_sha1':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    pbkdf_sha1=hash_algorithm[key]
                )
            elif key == 'sha1':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    sha1=hash_algorithm[key]
                )
            elif key == 'sha256':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    sha256=hash_algorithm[key]
                )
            elif key == 'sha512':
                hash_request = import_pb2.ImportDigitalTwinsRequest(
                    entities=entities,
                    sha512=hash_algorithm[key]
                )
        return hash_request
    except Exception as exception:
        return logger.logger_error(exception)


def validate_entity(e):
    """
    validate entity parameters
    :param e:
    :return: True or raises exception
    """
    try:
        kinds = [k.value for k in DigitalTwinKind]
        if e.kind not in kinds:
            raise TypeError("kind must be a member of DigitalTwinKind")
        states = [k.value for k in DigitalTwinState]
        if e.state not in states:
            raise TypeError("state must be a member of DigitalTwinState")
        if e.tags and not isinstance(e.tags, list):
            raise TypeError("tags must be a list")
        if not isinstance(e.password, import_pb2.PasswordCredential):
            raise TypeError("password must be an PasswordCredential object")
        if e.provider_user_info:
            if not isinstance(e.provider_user_info, list):
                raise TypeError("provider_user_info must be a list")
            for info in e.provider_user_info:
                if not isinstance(info, import_pb2.UserProvider):
                    raise TypeError(info + " : provider_user_info must be a UserProvider object")
        if e.properties and not isinstance(e.properties, import_pb2.ImportProperties):
            raise TypeError("properties must be an ImportProperties object")
        if e.metadata and not isinstance(e.metadata, import_pb2.UserMetadata):
            raise TypeError("metadata must be an UserMetadata object")
        if not isinstance(e, import_pb2.ImportDigitalTwin):
            raise TypeError("entity must be an ImportDigitalTwin object")
        return True
    except Exception as exception:
        return logger.logger_error(exception)


def divide_chunks(entities, n):
    """
    divide entities iin chunks
    :param entities: list of ImportDigitalTwin objects
    :param n: int
    :return:
    """
    if entities:
        for i in range(0, len(entities), n):
            yield entities[i:i + n]
