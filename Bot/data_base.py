from sqlalchemy import create_engine
from sqlalchemy import Column , String , LargeBinary
import sqlalchemy.orm as sqlorm
from cryptography.fernet import Fernet
key = Fernet.generate_key() 
cipher_suite = Fernet(key)




Base = sqlorm.declarative_base()
engine = create_engine('postgresql+psycopg2://postgres@localhost/chats_ids')
Session = sqlorm.sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__='User'
    name = Column(String, primary_key=True)
    chat_id = Column(LargeBinary)

def new_user(chat_id , name_user):
    encrypted_chat_id= cipher_suite.encrypt((bytes(str(chat_id) , encoding='utf8')))
    nuevo_usuario= User(name=name_user, chat_id=encrypted_chat_id )
    session.add(nuevo_usuario)
    

Base.metadata.create_all(engine)
hola = bytes(str(155415455), 'utf8')
hola = cipher_suite.encrypt(hola )
# print(type(hola))
# print(int(cipher_suite.decrypt(hola)))

new_user(155415455 , "pepe" )
hello = session.query(User).filter_by(name="pepe")

print(hello)
# print(cipher_suite.decrypt(hello))
