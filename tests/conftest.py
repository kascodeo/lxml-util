import pytest
from pathlib import Path
from lxml import etree
from lxmlutil.etree import ElementBase


@pytest.fixture
def parser():
    parser = etree.XMLParser()
    fallback = etree.ElementDefaultClassLookup(ElementBase)
    parser.set_element_class_lookup(fallback)
    return parser


@pytest.fixture
def data_path():
    return Path(__file__).parent / "data"


@pytest.fixture
def chart_path(data_path):
    return data_path / "chart1.xml"


@pytest.fixture
def rels_path(data_path):
    return data_path / "chart1.xml.rels"


@pytest.fixture
def e_(chart_path):
    return etree.parse(chart_path).getroot()


@pytest.fixture
def ns_c(e_):
    return e_.nsmap['c']


@pytest.fixture
def e_rels(parser, rels_path):
    return etree.parse(rels_path, parser=parser).getroot()


@pytest.fixture
def e(parser, chart_path):
    return etree.parse(chart_path, parser=parser).getroot()


@pytest.fixture
def ns_rels(e_rels):
    return e_rels.nsmap[None]


@pytest.fixture
def e_nsmap_empty(parser):
    return etree.XML('<self/>', parser)


@pytest.fixture
def e_has_ns_wo_prefix(parser):
    s = '<self xmlns="http://none/ns" xmlns:d="http://dee/ns"/>'
    return etree.XML(s, parser)


@pytest.fixture
def e_with_ns_attribute(e):
    e = e[-1]
    return e
