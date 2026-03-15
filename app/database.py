from app import db
from models.user import User

def init_db():
    db.create_all()
    # Создать первого admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', first_name='Admin', last_name='Adminov', 
                     password='admin123', role='admin')  # Хэшировать в проде
        db.session.add(admin)
        db.session.commit()
