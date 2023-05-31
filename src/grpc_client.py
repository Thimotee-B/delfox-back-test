import todo_pb2
import todo_pb2_grpc


class TodoGrpcClient:
    def __init__(self, channel):
        self.stub = todo_pb2_grpc.TodoServiceStub(channel)

    def create_todo(self, title: str, description: str = None):
        todo = todo_pb2.CreateTodoRequest(title=title, description=description)
        response = self.stub.CreateTodo(todo)
        return response

    def get_todo(self, id: int):
        request = todo_pb2.GetTodoRequest(id=id)
        response = self.stub.GetTodo(request)
        return response.todo

    def update_todo(self, id: int, title: str = None, description: str = None):
        todo = todo_pb2.Todo(id=id, title=title, description=description)
        request = todo_pb2.UpdateTodoRequest(todo=todo)
        response = self.stub.UpdateTodo(request)
        return response.todo

    def delete_todo(self, id: int):
        request = todo_pb2.DeleteTodoRequest(id=id)
        response = self.stub.DeleteTodo(request)
        return response.success
