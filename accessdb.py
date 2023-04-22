#!./dns/bin/python3
import sys
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String, create_engine, delete, insert, select, or_
from sqlalchemy.orm import declarative_base, Session

# --- DB structure
engine = create_engine("postgresql+psycopg2://dnspy:dnspy23./@localhost:5432/dnspy")
Base = declarative_base()

class Domains(Base):  
    __tablename__ = "domains" 
    
    id = Column(BigInteger, primary_key=True)  
    name = Column(String(255), nullable=False)
    ttl = Column(Integer, default=60)
    dclass = Column(String(2), default='IN')   
    type = Column(String(10))
    data = Column(String(255))


def get(qname, qclass, qtype):
    #print(qname)
    with Session(engine) as conn:
        stmt = (select(Domains)
                .filter(or_(Domains.name == qname, Domains.name == qname[:-1]))
                .filter(Domains.dclass == qclass)
                .filter(Domains.type == qtype)
        )
        result = conn.execute(stmt).all()
        return result

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
    Base.metadata.create_all(engine)
    try:
        argv = sys.argv[1::]
        d = argv[0]
        qtype = argv[1]
        rdata = argv[2]
    except:
        print('specify in order: domain qtype rdata')
        sys.exit()
    add(d, qtype, rdata)

