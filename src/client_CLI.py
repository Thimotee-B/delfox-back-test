import grpc

from grpc_client import TodoGrpcClient


def main():
    channel = grpc.insecure_channel('localhost:50051')
    client = TodoGrpcClient(channel)

    while True:
        print("\n1. Create Todo")
        print("2. Retrieve Todo")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Exit")

        choice = input("\nChoose an operation: ")
        try:
            if choice == '1':
                title = input("Enter title: ")
                description = input("Enter description: ")
                todo = client.create_todo(title, description)
                print(f'Created Todo: {todo}')
            elif choice == '2':
                todo_id = int(input("Enter Todo ID: "))
                todo = client.get_todo(todo_id)
                print(f'Retrieved Todo: {todo}')
            elif choice == '3':
                todo_id = int(input("Enter Todo ID: "))
                title = input("Enter new title: ")
                description = input("Enter new description: ")
                updated_todo = client.update_todo(todo_id, title, description)
                print(f'Updated Todo: {updated_todo}')
            elif choice == '4':
                todo_id = int(input("Enter Todo ID: "))
                success = client.delete_todo(todo_id)
                if success:
                    print('Todo deleted successfully')
                else:
                    print('Failed to delete Todo')
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please choose again.")

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
