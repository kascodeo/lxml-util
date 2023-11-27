Quick Start
===========

Python Support
--------------

This library supports these Python versions::
    3.11

This library may be compatible with earlier versions of python as well.


Installation
------------

Use pip to install this libary::

    pip install lxml-util
    
Introduction
------------

This is a python library providing the additional functionality to the lxml
python library.


Limitations of lxml library:

When e is object of lxml.etree.Element

    1. e.find() cannot handle prefixed tag names like "c:chart" and raises
        exceptions

    2. e.findall() cannot handle prefixed tag names like "c:chart" and raises
        exceptions

    3. e.makeelement() cannot handle prefixed tag names like "c:chart" and
        raises exceptions

    4. e.get() cannot handle prefixed attribute names like "r:id" and raises 
        exceptions
    
    5. e.set() cannot handle prefixed attribute names like "r:id" and raises 
        exceptions

    6. e does not have direct access to its children through the attributes. 
        e.chart gives attribute error though chart is child of element e

    7. No handy method in e object to find the local name. Have to use 
        etree.QName object to find the namespace of the element

    8. No handy method in e object to find the namespace. Have to use 
        etree.QName object to find the namespace of the element

    9. No handy method in e object to get the fully Qualified Name from
        prefixed tag name


Advantages of lxml-util library:
    All the above mentioned limitations are handled in this library

::
    
    from lxmlutil.etree import ElementBase
    from lxml import etree

    fallback = etree.ElementDefaultClassLookup(ElementBase)
    parser = etree.XMLParser()
    parser.set_element_class_lookup(fallback)

    e = etree.parse("path/to/xml/file", parser).getroot()

    e.nsmap
    #    {'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart', 
    #     'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 
    #     'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 
    #     'c16r2': 'http://schemas.microsoft.com/office/drawing/2015/06/chart'}

    # Object e now has additional methods defined in lxmlutil.etree.ElementBase
    # which are not available in lxml.etree.ElementBase

    e.qn("c:chart") # "{http://schemas.openxmlformats.org/drawingml/2006/chart}chart"

    e.ln            # "chartSpace"

    e.ns            # "http://schemas.openxmlformats.org/drawingml/2006/chart"

    e.find("c:chart")   # Gives error, cannot handle prefixed tag
    e.findqn("c:chart") # <Element {http://schemas.openxmlformats.org/drawingml/2006/chart}chart at 0x189d739f520>

    e.find("c:chart//c:areaChart") # Gives error, cannot handle prefixed tag
    e.findqn("c:chart//c:areaChart") # <Element {http://schemas.openxmlformats.org/drawingml/2006/chart}areaChart at 0x189d739f700>
    
    e.findall("c:chart//c:areaChart/c:axId") # Gives error, cannot handle prefixed tag
    e.findallqn("c:chart//c:areaChart/c:axId") # [<Element {http://schemas.openxmlformats.org/drawingml/2006/chart}axId at 0x189d739f7a0>, <Element {http://schemas.openxmlformats.org/drawingml/2006/chart}axId at 0x189d739f7f0>]
    
    e.get('r:id') # Gives error, cannot handled prefixed attribute names
    e.getqn('r:id') # resolves the prefixed name and gets the attribute

    e.set('r:id', "rId4") # Gives error, cannot handle prefixed attribute names
    e.setqn('r:id', "rId4") # resolves the prefixed name and sets the attribute

    e.makeelement('c:graph') # Gives error, cannot handle prefixed tag names
    e.meqn('c:graph') # <Element {http://schemas.openxmlformats.org/drawingml/2006/chart}graph at 0x189d739f7f0>

    # Dynamic attributes:
    e.c_chart               # equivalent to e.findqn('c:chart')
        # <Element {http://schemas.openxmlformats.org/drawingml/2006/chart}chart at 0x189d739f7f0>
        # c is prefix, chart is localname 

    e.c_chart__c_plotArea   # equivalent to e.findqn('c:chart/c:plotArea')
        # <Element {http://schemas.openxmlformats.org/drawingml/2006/chart}plotArea at 0x189d739f7a0>
        # Two underscores means './'

    e.c_chart___c_areaChart # equivalent to e.findqn('c:chart//c:areaChart')
        # <Element {http://schemas.openxmlformats.org/drawingml/2006/chart}areaChart at 0x189d739f520>
        # Three underscores means './/'

    e.c_externalData_r_id   # equivalent to e.findqn('c:externalData[@r:id]')
        # <Element {http://schemas.openxmlformats.org/drawingml/2006/chart}externalData at 0x189d739f8e0>
        # c is prefix for element tag
        # externalData is element localname
        # r is attribute prefix for element 'c:externalData'
        # id is attribute name for element  'c:externalData'

    e.___mc_Choice          # equivalent to e.findqn('.//mc:Choice')
        # <Element {http://schemas.openxmlformats.org/markup-compatibility/2006}Choice at 0x189d739fd90>
        #Though mc is not in nsmap of e, this method tries to find what could
        #be the namespace of mc prefix based on nsmap of children of element e
        


