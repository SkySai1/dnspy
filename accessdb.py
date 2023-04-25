#!./dns/bin/python3
from functools import lru_cache
import os
import sys
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String, create_engine, delete, insert, select, or_
from sqlalchemy.orm import declarative_base, Session

from confinit import getconf

def checkconnect(engine:create_engine):
    engine.connect()

# --- DB structure
Base = declarative_base()

class Domains(Base):  
    __tablename__ = "domains" 
    
    id = Column(BigInteger, primary_key=True)  
    name = Column(String(255), nullable=False)
    ttl = Column(Integer, default=60)
    dclass = Column(String(2), default='IN')   
    type = Column(String(10))
    data = Column(String(255))

class Cache(Base):  
    __tablename__ = "cache" 
    
    id = Column(BigInteger, primary_key=True)  
    name = Column(String(255), nullable=False)
    ttl = Column(Integer, default=60)
    dclass = Column(String(2), default='IN')   
    type = Column(String(10))
    data = Column(String(255))

class AccessDB:

    def __init__(self, engine):
        self.engine = engine   

    # -- Get from Authority zones
    #@lru_cache()
    def getA(self, qname, qclass, qtype):
        with Session(self.engine) as conn:
            stmt = (select(Domains)
                    .filter(or_(Domains.name == qname, Domains.name == qname[:-1]))
                    .filter(Domains.dclass == qclass)
                    .filter(Domains.type == qtype)
            )
            result = conn.execute(stmt).all()
            return result


    # -- Get from Cache    
    @lru_cache()
    def getC(self, qname, qclass, qtype):
        with Session(self.engine) as conn:
            stmt = (select(Domains)
                    .filter(or_(Domains.name == qname, Domains.name == qname[:-1]))
                    .filter(Domains.dclass == qclass)
                    .filter(Domains.type == qtype)
            )
            result = conn.execute(stmt).all()
            return result
    
    # -- Put to Cache
    def putC(self, rname, ttl, rclass, rtype, rdata):
        pass

    def add(d, qtype, rdata):
        with Session(engine) as conn:
            stmt = insert(Domains).values(
                name = d,
                type = qtype,
                data = rdata
            )
            conn.execute(stmt)
            conn.commit()
            conn.close()

if __name__ == "__main__":
    cpath = f"{os.path.abspath('./')}/dnspy.conf"
    _CONF = getconf(cpath)
    engine = create_engine(
        f"postgresql+psycopg2://{_CONF['dbuser']}:{_CONF['dbpass']}@{_CONF['dbhost']}:{_CONF['dbport']}/{_CONF['dbname']}"
    )
    Base.metadata.create_all(engine)
    try:
        argv = sys.argv[1::]
        d = argv[0]
        qtype = argv[1]
        rdata = argv[2]
    except:
        print('specify in order: domain qtype rdata')
        sys.exit()
    AccessDB.add(d, qtype, rdata)

