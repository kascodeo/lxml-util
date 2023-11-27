from lxmlutil.etree import ElementBase
import pytest
from unittest import mock


def test_elementbase_type_of_element(e):
    assert type(e) is ElementBase


def test_elementbase_ns_w_prefix(e, ns_c):
    assert e.ns == ns_c


def test_elementbase_ns_wo_prefix(e_rels, ns_rels):
    assert e_rels.ns == ns_rels


def test_elementbase_ns_of_no_namespace_element(parser):
    e = parser.makeelement('some')
    assert e.ns is None


def test_elementbase_ns_of_with_namespace_element(parser):
    e = parser.makeelement('{somenamespace}some')
    assert e.ns == "somenamespace"


def test_elementbase_qn_when_nsmap_is_empty(e_nsmap_empty):
    e = e_nsmap_empty
    assert e.nsmap == {}
    assert e.qn('some') == 'some'
    assert e.qn('some', {None: 'http://none/ns'}) == '{http://none/ns}some'
    assert e.qn('c:some', {'c': 'http://cee/ns'}) == '{http://cee/ns}some'
    pytest.raises(KeyError, e.qn, 'c:some')
    pytest.raises(KeyError, e.qn, 'c:some', {None: 'http://none/ns'})


def test_elementbase_qn_when_has_nsmap_wo_prefix(e_has_ns_wo_prefix):
    e = e_has_ns_wo_prefix
    assert None in e.nsmap
    assert 'd' in e.nsmap
    assert e.qn('some') == '{http://none/ns}some'
    assert e.qn('some', {None: 'http://none2/ns'}) == '{http://none2/ns}some'
    assert e.qn('c:some', {'c': 'http://cee/ns'}) == '{http://cee/ns}some'
    pytest.raises(KeyError, e.qn, 'c:some')
    pytest.raises(KeyError, e.qn, 'c:some', {None: 'http://none/ns'})
    assert e.qn('d:some') == '{http://dee/ns}some'


def test_elementbase_qn_no_prefix_no_nsmap_and_e_has_no_nsmap(parser):
    e = parser.makeelement('some')
    assert e.qn('just') == 'just'


def test_elementbase_qn_no_prefix_no_nsmap_and_e_has_nsmap(parser):
    e = parser.makeelement('some', nsmap={None: "somens"})
    assert e.qn('just') == '{somens}just'


def test_elementbase_qn_no_prefix_empty_nsmap_and_e_has_nsmap(parser):
    e = parser.makeelement('some', nsmap={None: "somens"})
    assert e.qn('just', nsmap={}) == 'just'


def test_elementbase_qn_no_prefix_none_in_nsmap_and_e_has_diff_ns_for_none(
        parser):
    e = parser.makeelement('some', nsmap={None: "somens"})
    assert e.qn('just', nsmap={None: "nsnone"}) == '{nsnone}just'


def test_elementbase_qn_no_prefix_no_nsmap_no_none_in_e_nsmap(parser):
    e = parser.makeelement('{nssome}some')
    assert e.qn('just') == 'just'


def test_elementbase_qn_with_prefix_no_nsmap_and_prefix_not_in_e_nsmap(
        parser):
    e = parser.makeelement('some', nsmap={None: "somens"})
    with pytest.raises(KeyError):
        e.qn('p:just')


def test_elementbase_qn_with_prefix_no_nsmap_and_prefix_in_e_nsmap(parser):
    e = parser.makeelement('some', nsmap={"p": "somens"})
    assert e.qn('p:just') == "{somens}just"


def test_elementbase_qn_with_prefix_nsmap_but_prefix_absent_prefix_in_e_nsmap(
        parser):
    e = parser.makeelement('some', nsmap={"p": "somens"})
    with pytest.raises(KeyError):
        e.qn('p:just', nsmap={'q': "qnamespace"})


def test_elementbase_qn_with_prefix_with_nsmap_prefix_present(parser):
    e = parser.makeelement('some', )
    e.qn('p:just', nsmap={'p': "pnamespace"}) == "{pnamespace}just"


def test_elementbase_ln_wo_prefix(e_has_ns_wo_prefix):
    assert e_has_ns_wo_prefix.ln == 'self'


def test_elementbase_ln_w_prefix(e):
    assert e.ln == 'chartSpace'


def test_elementbase_me_call_makeelement(e):
    tag = 'elem'
    attrib = {'a': '1', 'b': '2'}
    nsmap = e.nsmap
    ex = '3'
    ext = '4'
    val = e.makeelement(tag, attrib, nsmap, ex=ex, ext=ext)
    e.makeelement = mock.MagicMock(return_value=val)
    val2 = e.me(tag, attrib, nsmap, ex=ex, ext=ext)
    e.makeelement.assert_called_once_with(tag, attrib, nsmap, ex=ex, ext=ext)
    assert val2 is val


def test_elementbase_meqn_when_nsmap_is_empty(e_nsmap_empty):
    e = e_nsmap_empty
    pytest.raises(KeyError, e.meqn, 'c:foo')
    assert 'foo' == e.meqn('foo').tag
    assert '{http://Aaa/ns}foo' == e.meqn('a:foo',
                                          nsmap={'a': 'http://Aaa/ns'}).tag
    assert {'val': '1'} == e.meqn('a:foo', attrib={'val': '1'},
                                  nsmap={'a': 'http://Aaa/ns'}).attrib


def test_elementbase_meqn_when_has_prefix_no_none_in_nsmap(e, ns_c):
    pytest.raises(KeyError, e.meqn, 'd:foo')
    assert 'foo' == e.meqn('foo').tag
    assert '{http://Cee/ns}foo' == e.meqn('c:foo',
                                          nsmap={'c': 'http://Cee/ns'}).tag
    assert '{{{}}}foo'.format(ns_c) == e.meqn('c:foo').tag
    assert {'val': '1'} == e.meqn('a:foo', attrib={'val': '1'},
                                  nsmap={'a': 'http://Aaa/ns'}).attrib


def test_elementbase_meqn_when_has_prefix_none_in_nsmap(e_rels):
    e = e_rels
    assert '{{{}}}foo'.format(e.nsmap[None]) == e.meqn('foo').tag
    assert e.meqn('some', nsmap={None: 'http://bar'}).tag == '{http://bar}some'
    assert e.meqn('c:some', nsmap={
                  'c': 'http://bar'}).tag == '{http://bar}some'
    pytest.raises(KeyError, e.meqn, 'd:foo')


def test_elementbase_dump(e):
    from lxmlutil.etree import etree as et
    ret = "returnvalue"
    et.dump = mock.MagicMock(return_value=ret)
    val = e.dump()
    assert ret == val
    et.dump.assert_called_once_with(e)


def test_elementbase_deepcopy(e):
    from lxmlutil.etree import copy
    ret = "return_value"
    copy.deepcopy = mock.MagicMock(return_value=ret)
    val = e.deepcopy()
    assert val == ret
    copy.deepcopy.assert_called_once_with(e)


def test_elementbase_getqn(e_with_ns_attribute):
    e = e_with_ns_attribute
    assert "rId3" == e.getqn('r:id')
    e = e[-1]
    assert "0" == e.getqn('val')


def test_elementbase_setqn(e_with_ns_attribute):
    e = e_with_ns_attribute
    assert "rId3" == e.getqn('r:id')
    e.setqn('r:id', 'rId4')
    assert "rId4" == e.getqn('r:id')


def test_elementbase_findqn_no_prefix(e_rels):
    e = e_rels
    assert e.findqn('Relationship').ln == 'Relationship'
    assert e.findqn('Relationship').ns == e.nsmap[None]

    assert e.findqn('./Relationship').ln == 'Relationship'
    assert e.findqn('./Relationship').ns == e.nsmap[None]

    assert e.findqn('.//dummy').ln == 'dummy'
    assert e.findqn('.//dummy').ns == e.nsmap[None]


def test_elementbase_findqn_w_prefix_search_immediate_children(e):
    assert e.findqn('c:date1904').ln == 'date1904'
    assert e.findqn('.//a:ln').ln == 'ln'
    assert e.findqn('./c:date1904').ln == 'date1904'
    assert e.findqn('./c:date1904').ns == e.nsmap['c']
    assert e.findqn('.//c:date1904').ln == 'date1904'
    assert e.findqn('.//c:date1904').ns == e.nsmap['c']
    assert e.findqn('.//c:chart/c:plotArea').ln == 'plotArea'
    assert e.findqn('./c:chart//c:plotArea//c:strRef').ln == 'strRef'
    assert e.findqn('./c:chart//c:plotArea//c:strRef1') is None
    pytest.raises(SyntaxError, e.findqn, '/c:chart')


def test_elementbase_findqn_w_prefix_search_far_children(e):
    assert e.findqn('.//c:autoUpdate').ln == 'autoUpdate'
    assert e.findqn('./c:chart//').ln == 'autoTitleDeleted'
    ns = "http://schemas.microsoft.com/office/drawing/2014/chart"
    assert e.findqn('.//c16:uniqueId', namespaces={'c16': ns}).ln == 'uniqueId'
    pytest.raises(SyntaxError, e.findqn, '//c:chart')


def test_elementbase_findqn_w_prefix_search_attribute(e):
    assert e.findqn('c:lang[@val="en-US"]').ln == 'lang'
    assert e.findqn('.//c:externalData[@r:id]').ln == 'externalData'
    assert e.findqn('.//c:externalData[@r:id="rId3"]').ln == 'externalData'


def test_elementbase_findallqn_w_prefix_search_far_children(e):
    assert len(e.findallqn('.//c:ser')) == 2
    assert len(e.findallqn('.//c:axId')) == 4
    assert len(e.findallqn('.//c:axId3')) == 0
    pytest.raises(SyntaxError, e.findallqn, '//c:chart')


def test_elementbase_findallqn_w_prefix_search_immediate_children(e):
    e = e.findqn('.//c:areaChart')
    assert len(e.findallqn('./c:ser')) == 2
    assert len(e.findallqn('c:ser')) == 2
    pytest.raises(SyntaxError, e.findallqn, '/c:ser')


def test_elementbase_findallqn_w_prefix_search_attribute(e):
    assert len(e.findallqn('.//c:chart//c:axId[@val]')) == 4
    assert len(e.findallqn('.//c:axId[@val="505253232"]')) == 2


def test_elementbase__getattr__(e):
    e_extdata = e.findqn('./c:externalData')
    e_autoUpdate = e_extdata.findqn('./c:autoUpdate')

    assert e.c_externalData is e_extdata
    assert e.__c_externalData is e_extdata
    assert e.___c_externalData is e_extdata
    assert e.c_externalData_r_id is e_extdata
    assert e.__c_externalData_r_id is e_extdata
    assert e.___c_externalData_r_id is e_extdata

    assert e.c_externalDataNO is None
    assert e.__c_externalDataNO is None
    assert e.___c_externalDataNO is None
    assert e.c_externalDataNO_r_id is None
    assert e.__c_externalDataNO_r_id is None
    assert e.___c_externalDataNO_r_id is None

    assert e.c_externalData__c_autoUpdate is e_autoUpdate
    assert e.c_externalData___c_autoUpdate is e_autoUpdate

    assert e.c_externalData_r_id__c_autoUpdate_val is e_autoUpdate
