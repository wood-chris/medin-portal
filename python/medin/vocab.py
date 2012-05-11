# Created by Homme Zwaagstra
# 
# Copyright (c) 2012 GeoData Institute
# http://www.geodata.soton.ac.uk
# geodata@soton.ac.uk
# 
# Unless explicitly acquired and licensed from Licensor under another
# license, the contents of this file are subject to the Reciprocal
# Public License ("RPL") Version 1.5, or subsequent versions as
# allowed by the RPL, and You may not copy or use this file in either
# source code or executable form, except in compliance with the terms
# and conditions of the RPL.
# 
# All software distributed under the RPL is provided strictly on an
# "AS IS" basis, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, AND LICENSOR HEREBY DISCLAIMS ALL SUCH WARRANTIES,
# INCLUDING WITHOUT LIMITATION, ANY WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, QUIET ENJOYMENT, OR
# NON-INFRINGEMENT. See the RPL for specific language governing rights
# and limitations under the RPL.
# 
# You can obtain a full copy of the RPL from
# http://opensource.org/licenses/rpl1.5.txt or geodata@soton.ac.uk

"""
An interface to the portal vocabularies
"""

import skos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import Mapping


class Vocabularies(Mapping):
    _sessions = {}              # cached sessions
    def __init__(self, connstr):
        try:
            # try and retrieve a cached session
            self.session = self.__class__._sessions[connstr]()
        except KeyError:
            pass

        engine = create_engine(connstr) # get a handle on the vocabulary

        # get a session to the local database
        Session = self._sessions[connstr] = sessionmaker(bind=engine)
        self.session = Session()

    def __getitem__(self, key):
        obj = self.session.query(skos.Object).filter(skos.Object.uri == key).first()
        if obj is None:
            raise KeyError(key)
        return obj

    def __len__(self):
        return self.session.query(skos.Object).count()

    def __iter__(self):
        return iter(self.session.query(skos.Object.uri))

    def getMatchingConcept(self, term, collection):
        """
        Retrieve a matching term from a particular collection

        The match is case insensitive.
        """

        return self.session.query(skos.Concept)\
            .join(skos.Concept.collections)\
            .filter(skos.Collection.uri == collection)\
            .filter(skos.Concept.prefLabel.ilike(term)).first()
