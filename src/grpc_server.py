from concurrent import futures
import grpc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from todo_service import TodoService
import todo_pb2
import todo_pb2_grpc


class TodoServicer(todo_pb2_grpc.TodoServiceServicer):
    def __init__(self, service):
        self.service = service

    def CreateTodo(self, request, context):
        title = request.title
        description = request.description
        todo = self.service.create_todo(title, description)
        return todo_pb2.CreateTodoResponse(
            todo=todo_pb2.Todo(id=todo.id, title=todo.title, description=todo.description))

    def GetTodo(self, request, context):
        todo_id = request.id
        todo = self.service.get_todo(todo_id)
        if todo is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Todo not found')
            return todo_pb2.GetTodoResponse()
        else:
            return todo_pb2.GetTodoResponse(
                todo=todo_pb2.Todo(id=todo.id, title=todo.title, description=todo.description))

    def UpdateTodo(self, request, context):
        todo_id = request.todo.id
        title = request.todo.title
        description = request.todo.description
        todo = self.service.update_todo(todo_id, title, description)
        if todo is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Todo not found')
            return todo_pb2.UpdateTodoResponse()
        else:
            return todo_pb2.UpdateTodoResponse(
                todo=todo_pb2.Todo(id=todo.id, title=todo.title, description=todo.description))

    def DeleteTodo(self, request, context):
        todo_id = request.id
        success = self.service.delete_todo(todo_id)
        return todo_pb2.DeleteTodoResponse(success=success)


# TODO: Implement gRPC method

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Create the database and the database session
    engine = create_engine('sqlite:///todos.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    service = TodoService(session)
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoServicer(service), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
