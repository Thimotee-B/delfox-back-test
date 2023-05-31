from sqlalchemy.orm import Session
from models import Todo


class TodoService:
    def __init__(self, session: Session):
        self.session = session

    def create_todo(self, title: str, description: str = None):
        new_todo = Todo(title=title, description=description)
        self.session.add(new_todo)
        self.session.commit()
        return new_todo

    def get_todo(self, id: int):
        todo = self.session.query(Todo).filter_by(id=id).first()
        return todo

    def update_todo(self, id: int, title: str = None, description: str = None):
        todo = self.session.query(Todo).filter_by(id=id).first()
        if not todo:
            return None
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        self.session.commit()
        return todo

    def delete_todo(self, id: int):
        todo = self.session.query(Todo).filter_by(id=id).first()
        if not todo:
            return False
        self.session.delete(todo)
        self.session.commit()
        return True
