import os

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tardisatomic.alchemy import Base, Atom
import tardisatomic

basic_atomic_data_fname = os.path.join(tardisatomic.__path__[0], 'data',
                                       'basic_atomic_data.csv')

class AtomicDatabase(object):

    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        self.session = sessionmaker(bind=self.engine)()

        self._init_empty_db()

    def _init_empty_db(self):
        basic_atomic_data = pd.read_csv(basic_atomic_data_fname)
        atoms = []
        for i, row in basic_atomic_data.iterrows():
            atoms.append(Atom(atomic_number=row.z, name=row.name,
                              symbol=row.symbol, group=row.group,
                              period=row.period))
        self.session.add_all(atoms)
        self.session.commit()







