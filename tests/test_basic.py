import pytest
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


@pytest.fixture
def engine():
    return create_engine("sqlite+libsql://")


@pytest.fixture
def session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_connection(engine):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_create_table(session):
    with session.connection() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        )
        assert result.scalar() == "users"


def test_insert_and_query(session):
    user = User(name="Test User", email="test@example.com")
    session.add(user)
    session.commit()

    queried_user = session.query(User).first()
    assert queried_user.name == "Test User"
    assert queried_user.email == "test@example.com"


def test_update(session):
    user = User(name="Test User", email="test@example.com")
    session.add(user)
    session.commit()

    user.name = "Updated User"
    session.commit()

    updated_user = session.query(User).first()
    assert updated_user.name == "Updated User"


def test_delete(session):
    user = User(name="Test User", email="test@example.com")
    session.add(user)
    session.commit()

    session.delete(user)
    session.commit()

    assert session.query(User).count() == 0
