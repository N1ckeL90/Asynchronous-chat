from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

engine = create_engine('sqlite:///chat.db', echo=False, pool_recycle=7200)

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True, nullable=False)
    info = Column(String(255))

    sessions_history = relationship("ClientHistory", back_populates='clients')
    contacts = relationship("Contact", back_populates='clients')

    def __init__(self, login, info):
        self.login = login
        self.info = info

    def __repr__(self):
        return f'Client(login={self.login}, info={self.info})'


class ClientHistory(Base):
    __tablename__ = 'sessions_history'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    sign_in_time = Column(DateTime, default=datetime.now)
    ip_address = Column(String(16), nullable=False)

    clients = relationship('Client', back_populates='sessions_history')

    def __init__(self, client_id, sign_in_time, ip_address):
        self.client_id = client_id
        self.sign_in_time = sign_in_time
        self.ip_address = ip_address

    def __repr__(self):
        return f'Session(id={self.id}, client_id={self.client_id}, sign_in_time={self.sign_in_time})'


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    id_owner = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)

    clients = relationship('Client', back_populates='contacts')

    def __init__(self, id_owner, client_id):
        self.id_owner = id_owner
        self.client_id = client_id

    def __repr__(self):
        return f'Contact(id={self.id}, id_owner={self.id_owner}, client_id={self.client_id})'


metadata = Base.metadata
# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()
# Тест записи
client1 = Client('guest', 'info')
session.add(client1)
# Тест чтения
q_client1 = session.query(Client).first()
print(q_client1)
session.commit()
