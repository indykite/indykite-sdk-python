import json
import time

from indykite_sdk.identity import IdentityClient
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import ImportDigitalTwin, ImportDigitalTwinsResponse, ImportDigitalTwinSuccess, ImportDigitalTwinsRequest, ImportDigitalTwinError
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import PasswordCredential, PasswordHash, Bcrypt, SHA256, UserProvider
from indykite_sdk.indykite.identity.v1beta2.import_pb2 import Email as EmailIdentity
from google.protobuf.json_format import MessageToDict
from helpers import data


def test_import_digital_twin_wrong_twin_id():
    digital_twin_id = "gid:AAAAA2luZHlraURlgAADDwAAAAI"
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        id=digital_twin_id,
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test2101@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is not None
    for r in response:
        assert isinstance(r, ImportDigitalTwinsResponse)
        adict = MessageToDict(r)
        res = json.dumps(adict)
        assert "invalid DigitalTwin ID" in res
        assert isinstance(r.results[0].error, ImportDigitalTwinError)


def test_import_digital_twin_success():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test"+right_now+"@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    for r in response:
        assert isinstance(r, ImportDigitalTwinsResponse)
        adict = MessageToDict(r)
        res = json.dumps(adict)
        assert "success" in res
        assert isinstance(r.results[0].success, ImportDigitalTwinSuccess)


def test_import_digital_twin_empty():
    digital_twin_id = "gid:AAAAFUu7KoHY9E3Pi1p0LnfOELg"
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        id=digital_twin_id,
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test2101@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    def mocked_import_digital_twin(request: ImportDigitalTwinsRequest):
        return None

    client.stub.ImportDigitalTwins = mocked_import_digital_twin
    response = client.import_digital_twins(entities, hash_algorithm)

    assert response is None


def test_import_digital_twin_exception():
    tenant_id = data.get_tenant()
    entities = "entities"
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_sha256():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"sha256": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_bcrypt():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"bcrypt": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_hmac_sha512():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"hmac_sha512": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_hmac_sha256():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"hmac_sha256": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_md5():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"md5": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_pbkdf2_sha256():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"pbkdf2_sha256": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_pbkdf_sha1():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"pbkdf_sha1": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_sha1():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"sha1": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_sha512():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"sha512": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_standard_scrypt():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"sha256": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_scrypt():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"scrypt": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_hmac_md5():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"hmac_md5": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_hmac_sha1():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = [ImportDigitalTwin(
        tenant_id=tenant_id,
        kind="DIGITAL_TWIN_KIND_PERSON",
        state="DIGITAL_TWIN_STATE_ACTIVE",
        password=PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
    )
    ]
    hash_algorithm = {"hmac_sha1": "square=14"}

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_kind():
    entities = []

    class Entity:
        kind = 12
        state = 12
        tags = "tags"
        password = "password"
        provider_user_info = "user_info"
        properties = "properties"
        metadata = "metadata"

    entity = Entity()
    entities.append(entity)
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_state():
    entities = []

    class Entity:
        kind = 0
        state = 12
        tags = []
        password = "password"
        provider_user_info = "user_info"
        properties = "properties"
        metadata = "metadata"

    entity = Entity()
    entities.append(entity)
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_tags():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = []

    class Entity:
        kind = 1
        state = 1
        tags = "tags"
        password = "password"
        provider_user_info = "user_info"
        properties = "properties"
        metadata = "metadata"

    entity = Entity()
    entities.append(entity)
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_password():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = []

    class Entity:
        kind = 1
        state = 1
        tags = []
        password = "password"
        provider_user_info = "user_info"
        properties = "properties"
        metadata = "metadata"

    entity = Entity()
    entities.append(entity)
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_user_info():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = []

    class Entity:
        kind = 1
        state = 1
        tags = []
        password = PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
        provider_user_info = "user_info"
        properties = "properties"
        metadata = "metadata"

    entity = Entity()
    entities.append(entity)
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None

def test_import_digital_twin_non_valid_user_info2():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = []

    class Entity:
        kind = 1
        state = 1
        tags = []
        password = PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
        provider_user_info = ["user_info"]
        properties = "properties"
        metadata = "metadata"

    entity = Entity()
    entities.append(entity)
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_non_valid_properties():
    right_now = str(int(time.time()))
    tenant_id = data.get_tenant()
    entities = []

    class Entity:
        kind = 1
        state = 1
        tags = []
        password = PasswordCredential(
            email=EmailIdentity(
                email="test" + right_now + "@example.com",
                verified=True
            ),
            value="password"
        )
        provider_user_info = [UserProvider(uid="12546",provider_id="1245",email="example@example.com",display_name="display_name",photo_url="")]
        properties = "properties"
        metadata = "metadata"

    entity = Entity()
    entities.append(entity)
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(entities, hash_algorithm)
    assert response is None


def test_import_digital_twin_no_entity():
    hash_algorithm = None

    client = IdentityClient()
    assert client is not None

    response = client.import_digital_twins(None, hash_algorithm)
    assert response is None
