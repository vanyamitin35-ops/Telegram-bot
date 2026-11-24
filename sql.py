from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.orm import Session as DBSession # Переименовано, чтобы избежать конфликта с sessionmaker
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

# Базовый класс для декларативных моделей
Base = declarative_base()

class Orders(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False) # user_id скорее всего должен быть обязательным
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False) # Или Float, если цена может быть дробной

    # Добавление отношений к Confirmed_Orders
    # Это позволит обращаться к подтвержденным заказам из объекта Orders
    # lazy='joined' загружает связанные объекты сразу
    confirmed_entry = relationship("Confirmed_Orders", back_populates="original_order", uselist=False)

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, name='{self.name}', price={self.price})>"
    
    
class Confirmed_Orders(Base):
    __tablename__ = "confirmed_orders"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    # Confirmed_Orders ссылается на конкретный подтвержденный заказ
    # из таблицы Orders через его primary_key.
    # user_id и price в Confirmed_Orders теперь будут просто копиями значений
    # из оригинального заказа, или могут быть получены через relationship.
    
    # ForeignKey к id конкретного заказа в таблице Orders
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True) # unique=True, если один заказ может быть подтвержден только один раз
    
    # user_id и price из оригинального заказа, если они должны быть напрямую доступны
    # здесь, а не через original_order relationship.
    user_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False) # Или Float

    # Время подтверждения. Рекомендуется использовать тип DateTime для дат/времени.
    time = Column(DateTime, default=datetime.utcnow, nullable=False) # Записываем UTC время создания

    # Добавляем отношение к оригинальному заказу
    original_order = relationship("Orders", back_populates="confirmed_entry")

    def __repr__(self):
        return (f"<Confirmed_Order(id={self.id}, order_id={self.order_id}, "
                f"user_id={self.user_id}, name='{self.name}', price={self.price}, time='{self.time}')>")
        
        
class feedbacks(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    feedback = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return (f"<feedbacks(id={self.id}, user_id={self.user_id}, feedback={self.feedback}, time={self.time})>")
    
    
class deleted_orders(Base):
    __tablename__ = "deleted_orders"
    
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, nullable=False)
    deleted_orders = Column(String,nullable=False)
    
    def __repr__(self):
        return (f"<deleted_orders(id={self.id}, user_id={self.user_id}, deleted_orders={self.deleted_orders})>")

# Настройки базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///orders.db" 
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True) # echo=True для вывода SQL-запросов в консоль

# Создание всех таблиц
Base.metadata.create_all(engine)

# Создание фабрики сессий
# SessionLocal - это класс, экземпляр которого будет использоваться для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
# Обычно используется как зависимость в FastAPI или как контекстный менеджер
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        

       

        
        
