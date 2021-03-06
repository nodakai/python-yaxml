# Quoted from http://relaxng.org/spec-20011203.html
#
# RELAX NG Specification
# Committee Specification 3 December 2001
#
# This version:
#   Committee Specification: 3 December 2001
#
# Previous versions:
#   Committee Specification: 11 August 2001
#
# Editors:
#   James Clark <jjc@jclark.com>, MURATA Makoto <EB2M-MRT@asahi-net.or.jp>
#
# Copyright (c) The Organization for the Advancement of Structured Information Standards [OASIS]
# 2001. All Rights Reserved.
#
# This document and translations of it may be copied and furnished to others, and derivative works
# that comment on or otherwise explain it or assist in its implementation may be prepared, copied,
# published and distributed, in whole or in part, without restriction of any kind, provided that the
# above copyright notice and this paragraph are included on all such copies and derivative works.
# However, this document itself may not be modified in any way, such as by removing the copyright
# notice or references to OASIS, except as needed for the purpose of developing OASIS
# specifications, in which case the procedures for copyrights defined in the OASIS Intellectual
# Property Rights document must be followed, or as required to translate it into languages other
# than English.
#
# The limited permissions granted above are perpetual and will not be revoked by OASIS or its
# successors or assigns.
#
# This document and the information contained herein is provided on an "AS IS" basis and OASIS
# DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTY THAT THE
# USE OF THE INFORMATION HEREIN WILL NOT INFRINGE ANY RIGHTS OR ANY IMPLIED WARRANTIES OF
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

DATA = '''
<grammar datatypeLibrary="http://www.w3.org/2001/XMLSchema-datatypes"
  ns="http://relaxng.org/ns/structure/1.0"
  xmlns="http://relaxng.org/ns/structure/1.0">

  <start>
    <ref name="pattern"/>
  </start>

  <define name="pattern">
    <choice>
      <element name="element">
        <choice>
          <attribute name="name">
            <data type="QName"/>
          </attribute>
          <ref name="open-name-class"/>
        </choice>
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="attribute">
        <ref name="common-atts"/>
        <choice>
          <attribute name="name">
            <data type="QName"/>
          </attribute>
          <ref name="open-name-class"/>
        </choice>
        <interleave>
          <ref name="other"/>
          <optional>
            <ref name="pattern"/>
          </optional>
        </interleave>
      </element>
      <element name="group">
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="interleave">
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="choice">
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="optional">
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="zeroOrMore">
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="oneOrMore">
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="list">
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="mixed">
        <ref name="common-atts"/>
        <ref name="open-patterns"/>
      </element>
      <element name="ref">
        <attribute name="name">
          <data type="NCName"/>
        </attribute>
        <ref name="common-atts"/>
      </element>
      <element name="parentRef">
        <attribute name="name">
          <data type="NCName"/>
        </attribute>
        <ref name="common-atts"/>
      </element>
      <element name="empty">
        <ref name="common-atts"/>
        <ref name="other"/>
      </element>
      <element name="text">
        <ref name="common-atts"/>
        <ref name="other"/>
      </element>
      <element name="value">
        <optional>
          <attribute name="type">
            <data type="NCName"/>
          </attribute>
        </optional>
        <ref name="common-atts"/>
        <text/>
      </element>
      <element name="data">
        <attribute name="type">
          <data type="NCName"/>
        </attribute>
        <ref name="common-atts"/>
        <interleave>
          <ref name="other"/>
          <group>
            <zeroOrMore>
              <element name="param">
                <attribute name="name">
                  <data type="NCName"/>
                </attribute>
                <text/>
              </element>
            </zeroOrMore>
            <optional>
              <element name="except">
                <ref name="common-atts"/>
                <ref name="open-patterns"/>
              </element>
            </optional>
          </group>
        </interleave>
      </element>
      <element name="notAllowed">
        <ref name="common-atts"/>
        <ref name="other"/>
      </element>
      <element name="externalRef">
        <attribute name="href">
          <data type="anyURI"/>
        </attribute>
        <ref name="common-atts"/>
        <ref name="other"/>
      </element>
      <element name="grammar">
        <ref name="common-atts"/>
        <ref name="grammar-content"/>
      </element>
    </choice>
  </define>

  <define name="grammar-content">
    <interleave>
      <ref name="other"/>
      <zeroOrMore>
        <choice>
          <ref name="start-element"/>
          <ref name="define-element"/>
          <element name="div">
            <ref name="common-atts"/>
            <ref name="grammar-content"/>
          </element>
          <element name="include">
            <attribute name="href">
              <data type="anyURI"/>
            </attribute>
            <ref name="common-atts"/>
            <ref name="include-content"/>
          </element>
        </choice>
      </zeroOrMore>
    </interleave>
  </define>

  <define name="include-content">
    <interleave>
      <ref name="other"/>
      <zeroOrMore>
        <choice>
          <ref name="start-element"/>
          <ref name="define-element"/>
          <element name="div">
            <ref name="common-atts"/>
            <ref name="include-content"/>
          </element>
        </choice>
      </zeroOrMore>
    </interleave>
  </define>

  <define name="start-element">
    <element name="start">
      <ref name="combine-att"/>
      <ref name="common-atts"/>
      <ref name="open-pattern"/>
    </element>
  </define>

  <define name="define-element">
    <element name="define">
      <attribute name="name">
        <data type="NCName"/>
      </attribute>
      <ref name="combine-att"/>
      <ref name="common-atts"/>
      <ref name="open-patterns"/>
    </element>
  </define>

  <define name="combine-att">
    <optional>
      <attribute name="combine">
        <choice>
          <value>choice</value>
          <value>interleave</value>
        </choice>
      </attribute>
    </optional>
  </define>

  <define name="open-patterns">
    <interleave>
      <ref name="other"/>
      <oneOrMore>
        <ref name="pattern"/>
      </oneOrMore>
    </interleave>
  </define>

  <define name="open-pattern">
    <interleave>
      <ref name="other"/>
      <ref name="pattern"/>
    </interleave>
  </define>

  <define name="name-class">
    <choice>
      <element name="name">
        <ref name="common-atts"/>
        <data type="QName"/>
      </element>
      <element name="anyName">
        <ref name="common-atts"/>
        <ref name="except-name-class"/>
      </element>
      <element name="nsName">
        <ref name="common-atts"/>
        <ref name="except-name-class"/>
      </element>
      <element name="choice">
        <ref name="common-atts"/>
        <ref name="open-name-classes"/>
      </element>
    </choice>
  </define>

  <define name="except-name-class">
    <interleave>
      <ref name="other"/>
      <optional>
        <element name="except">
          <ref name="open-name-classes"/>
        </element>
      </optional>
    </interleave>
  </define>

  <define name="open-name-classes">
    <interleave>
      <ref name="other"/>
      <oneOrMore>
        <ref name="name-class"/>
      </oneOrMore>
    </interleave>
  </define>

  <define name="open-name-class">
    <interleave>
      <ref name="other"/>
      <ref name="name-class"/>
    </interleave>
  </define>

  <define name="common-atts">
    <optional>
      <attribute name="ns"/>
    </optional>
    <optional>
      <attribute name="datatypeLibrary">
        <data type="anyURI"/>
      </attribute>
    </optional>
    <zeroOrMore>
      <attribute>
        <anyName>
          <except>
            <nsName/>
            <nsName ns=""/>
          </except>
        </anyName>
      </attribute>
    </zeroOrMore>
  </define>

  <define name="other">
    <zeroOrMore>
      <element>
        <anyName>
          <except>
            <nsName/>
          </except>
        </anyName>
        <zeroOrMore>
          <choice>
            <attribute>
              <anyName/>
            </attribute>
            <text/>
            <ref name="any"/>
          </choice>
        </zeroOrMore>
      </element>
    </zeroOrMore>
  </define>

  <define name="any">
    <element>
      <anyName/>
      <zeroOrMore>
        <choice>
          <attribute>
            <anyName/>
          </attribute>
          <text/>
          <ref name="any"/>
        </choice>
      </zeroOrMore>
    </element>
  </define>

</grammar>
'''.strip()
