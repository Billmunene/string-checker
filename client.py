import os

def search_string_in_file(file_path, search_string):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() == search_string:
                    return True
        return False
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    # Determine the file path based on the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '200k.txt')
    
    search_string = input("Enter the string to search for in the file: ").strip()

    if search_string_in_file(file_path, search_string):
        print("STRING EXISTS")
    else:
        print("STRING NOT FOUND")
