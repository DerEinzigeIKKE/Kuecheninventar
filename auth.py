import bcrypt
from sqlalchemy.orm import Session
from database import User

def hash_password(password: str) -> str:
    """
    Erzeugt einen sicheren Hash aus dem Klartext-Passwort.
    
    Args:
        password (str): Das Passwort im Klartext.
        
    Returns:
        str: Das gehashte Passwort als String.
    """
    # Generiert einen Salt und hasht das Passwort
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    """
    Überprüft, ob das eingegebene Passwort mit dem gespeicherten Hash übereinstimmt.
    
    Args:
        plain_password (str): Das eingegebene Passwort.
        hashed_password (str): Der gespeicherte Hash aus der Datenbank.
        
    Returns:
        bool: True, wenn das Passwort korrekt ist, sonst False.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(db: Session, username: str, password: str) -> bool:
    """
    Registriert einen neuen Benutzer in der Datenbank.
    
    Args:
        db (Session): Die Datenbank-Sitzung.
        username (str): Der gewünschte Benutzername.
        password (str): Das gewünschte Passwort.
        
    Returns:
        bool: True bei erfolgreicher Registrierung, False wenn der Benutzername existiert.
    """
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return False
    
    new_user = User(
        username=username,
        password_hash=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True

def authenticate_user(db: Session, username: str, password: str):
    """
    Authentifiziert einen Benutzer.
    
    Args:
        db (Session): Die Datenbank-Sitzung.
        username (str): Der Benutzername.
        password (str): Das Passwort.
        
    Returns:
        User: Das User-Objekt bei Erfolg, sonst None.
    """
    user = db.query(User).filter(User.username == username).first()
    if user and check_password(password, user.password_hash):
        return user
    return None
