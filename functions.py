import os

def delete_file(folder_path,filename):
    file_path = os.path.join(folder_path,filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted file:{file_path}")
            return True
        except OSError as error:
            print(f"Unable to delete:{file_path} . {error}")

    else:
        print(f"The {file_path} does not exist.")
        return False

def create_file(folder_path,filename):
    file_path = os.path.join(folder_path,filename)
    if os.path.exists(file_path):
        print(f"The {file_path} already exists!")
        return False

    else:
        try:
            os.makedirs(folder_path,exist_ok=True)
            with open(file_path, 'w') as File:
                pass

            print(f"Created empty file in : {file_path}")
            return True

        except OSError as error:
            print(f"Failed to create the empty file:{file_path} due to {error}")
            return False

def update_file(folder_path,filename,txt,option):
    file_path = os.path.join(folder_path,filename)

    try:
        if (option == 0):
            with open(file_path, 'r+') as File: # il deschide cu write pentru a goli fisierul
                if option == 0:
                    File.truncate(0)

                File.write(txt + "\n")
                print(f"New content has been written in file: {file_path}")
                return True

    except OSError as error:
        print(f"Unable to update the :{file_path} due to {error}")
        return False






