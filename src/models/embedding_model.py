from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import numpy as np
from sqlalchemy.orm import Session
# Configuração do banco de dados
DATABASE_URL = "sqlite:///src/database/agent.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class EmbeddingModel(Base):
    __tablename__ = "embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    vector = Column(LargeBinary)
    description = Column(String, nullable=True)

    def __repr__(self) -> str:
       return f"User(id={self.id!r}, title={self.title!r}, vector={self.vector!r}, description={self.description!r})"

# Base.metadata.create_all(engine)

def insert_embedding(session, title: str, vector: np.ndarray, description: str):
    db_embedding = EmbeddingModel(
        title=title,
        vector=vector.tobytes(),
        description=description
    )
    session.add(db_embedding)
    session.commit()
    session.refresh(db_embedding)
    return db_embedding

session = SessionLocal()
example_vector = np.array([np.random.rand(128).astype(np.float32)])
print("ENTRADA", example_vector)
inserted_embedding = insert_embedding(session, "Exemplo", example_vector, "Este é um embedding de exemplo.")
print(f"Inserido: {inserted_embedding.id}, {inserted_embedding.title}")
session.close()


session = Session(engine)

stmt = select(EmbeddingModel).where(EmbeddingModel.id.in_([10]))

for user in session.scalars(stmt):
    print(user.vector)
    v = np.frombuffer(user.vector, np.float64)
    print(v)