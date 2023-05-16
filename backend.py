from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base#, Session


Base = declarative_base()
engine = create_engine('sqlite:///zaidimai.db')
Session = sessionmaker(bind=engine)
session = Session()

benroji_lentele = Table("bendri", Base.metadata,
    Column('zaidimas_id', Integer, ForeignKey('zaidimai.id')),
    Column('zanras_id', Integer, ForeignKey('zanrai.id'))    
)

class Zaidimas(Base):
    __tablename__ = "zaidimai"
    
    id = Column(Integer, primary_key= True)
    zaidimo_pavadinimas = Column(String)
    kurejo_id = Column(Integer, ForeignKey("kurejai.id"))
    youtube_link = Column(String)

    kurejas = relationship('Kurejas', back_populates='zaidimai')
    zanrai = relationship('Zanras', secondary=benroji_lentele, back_populates='zaidimai')

class Kurejas(Base):
    __tablename__ = "kurejai"

    id = Column(Integer, primary_key=True)
    kurejo_pavadinimas = Column(String)

    zaidimai = relationship("Zaidimas", back_populates="kurejas")

class Zanras(Base):
    __tablename__ = "zanrai"

    id = Column(Integer, primary_key=True)
    zanro_pavadinimas = Column(String)

    zaidimai = relationship("Zaidimas", secondary=benroji_lentele, back_populates="zanrai")


def add_game(zaidimo_pavadinimas, kurejas, zanras, youtube_link):
    kurejas_obj = session.query(Kurejas).filter_by(kurejo_pavadinimas=kurejas).first()
    if not kurejas_obj:
        kurejas_obj = Kurejas(kurejo_pavadinimas=kurejas)

    zanras_obj = session.query(Zanras).filter_by(zanro_pavadinimas=zanras).first()
    if not zanras_obj:
        zanras_obj = Zanras(zanro_pavadinimas=zanras)

    new_game = Zaidimas(zaidimo_pavadinimas=zaidimo_pavadinimas, kurejas=kurejas_obj, zanrai=[zanras_obj], youtube_link=youtube_link)
    session.add(new_game)
    session.commit()

def esami_kurejai():
    with Session() as session:
        kurejai = session.query(Kurejas).all()
        return [kurejo.kurejo_pavadinimas for kurejo in kurejai]
    
def esami_zanrai():
    with Session() as session:
        zanrai = session.query(Zanras).all()
        return [zanras.zanro_pavadinimas for zanras in zanrai]

Base.metadata.create_all(engine)