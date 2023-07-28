from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # __table__args = ()
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10), db.CheckConstraint('length(phone_number) = 10' ))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if(len(phone_number) != 10):
            raise ValueError("Phone number must be 10 digits.")
        return phone_number
    
    @validates('name')
    def validate_name(self, key, name): 
        names = db.session.query(Author.name).all()
        if not name: 
            raise ValueError('name is required')
        elif(name in names): 
            raise ValueError('The name must be unique')
        return name 
        

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    
    @validates('content')
    def validate_content(self, key, content): 
        if(len(content) < 250):
            raise ValueError('post content must be at least 250 chars')
        return content  
    
    @validates('summary')
    def validate_summary(self, key, summary): 
        if(len(summary) >= 250): 
            raise ValueError('summary cant be longer than 250 chars')
        return summary 
    @validates('category')
    def validate_category(self, key, category):
        c = ['Fiction', 'Non-Fiction'] 
        if category not in c:
            raise ValueError('category must be fiction or non-fiction')
        return category
    
    @validates('title') 
    def validate_title(self, key, title): 
        t = ["Won't Believe", "Secret", "Top", "Guess"]
        raise ValueError('must be click bait') if title not in t else None 
    
            
      
            


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
