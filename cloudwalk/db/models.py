from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    status = Column(String)
    batch = Column(Integer)
    credit_limit = Column(Integer)
    interest_rate = Column(Integer)
    denied_reason = Column(String)
    denied_at = Column(DateTime)

    loans = relationship("Loan", back_populates="client")


class Loan(Base):
    __tablename__ = 'loans'

    loan_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('clients.user_id'))
    created_at = Column(DateTime)
    due_at = Column(DateTime)
    paid_at = Column(DateTime)
    status = Column(String)
    loan_amount = Column(Float)
    tax = Column(Float)
    due_amount = Column(Float)
    amount_paid = Column(Float)

    client = relationship("Client", back_populates="loans")
