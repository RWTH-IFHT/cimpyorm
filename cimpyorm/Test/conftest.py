import pytest
import os
import logging

# Keep import for _CONFIGPATH - otherwise get_path fails because cimpyorm/__init__.py locals aren't present
from cimpyorm import get_path
import cimpyorm.Parser
from cimpyorm.api import load
from cimpyorm.Backend.auxiliary import HDict
logging.disable(logging.CRITICAL)


@pytest.fixture(scope="session")
def full_grid():
    try:
        path = os.path.join(get_path("DATASETROOT"), "FullGrid")
    except KeyError:
        pytest.skip(f"Dataset path not configured")
    if not os.path.isdir(path) or not os.listdir(path):
        pytest.skip("Dataset 'FullGrid' not present.")
    else:
        return path


@pytest.fixture(scope="module")
def acquire_db():
    engine, session = cimpyorm.Parser.bind_db(database=":memory:")
    return engine, session


@pytest.fixture(scope="session")
def load_test_db():
    """
    Returns a session and a model for a database that's only supposed to be read from
    :return: session, m
    """
    try:
        path = os.path.join(get_path("DATASETROOT"), "FullGrid", "StaticTest.db")
        session, m = load(path)
        return session, m
    except (KeyError, FileNotFoundError):
        pytest.skip("StaticTest.db not present.")


@pytest.fixture(scope="session")
def dummy_source():
    try:
        path = os.path.join(get_path("DATASETROOT"), "FullGrid", "20171002T0930Z_BE_EQ_4.xml")
    except KeyError:
        pytest.skip(f"Dataset path not configured")
    if not os.path.isfile(path):
        pytest.skip("Dataset 'FullGrid' not present.")
    from cimpyorm.Backend.Source import SourceInfo
    ds = SourceInfo(source_file=path, source_id=1)
    return ds


@pytest.fixture(scope="session")
def dummy_nsmap():
    nsmap = HDict({'cim': 'http://iec.ch/TC57/2013/CIM-schema-cim16#',
                   'entsoe': 'http://entsoe.eu/CIM/SchemaExtension/3/1#',
                   'md': 'http://iec.ch/TC57/61970-552/ModelDescription/1#',
                   'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
    return nsmap