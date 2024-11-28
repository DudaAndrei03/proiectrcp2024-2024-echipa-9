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

def create_file(folder_path,filename,content):
    file_path = os.path.join(folder_path,filename)
    if os.path.exists(file_path):
        print(f"The {file_path} already exists!")
        return False

    else:
        try:
            os.makedirs(folder_path,exist_ok=True)
            with open(file_path,'w') as File:
                File.write(content)
                return True

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


def read_file(folder_path,filename):
    file_path = os.path.join(folder_path, filename)
    try:
        with open(filename,'rb') as file: #deschid in binar pt a putea trimite in retea->trebuie citit cu 'wb'
            content=file.read()
            return content
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return False


def create_dir(path):
    os.mkdir(path,mode=0o777)


def generate_code(method,content):
    code=None
    if method==1:
        if content: #succes
            code=2
        else:
            code=4
    if method == 2:
        if content:
            code=2
        else:
            code=4
    if method == 3:
        if content:
            code=2 #creat
        else:
            code=4
    return code


def rename_file(old_name, new_name):
        # Check if the source file exists
        if not os.path.exists(old_name):
            return False

        # Check if the destination file already exists
        if os.path.exists(new_name) == False:
            os.rename(old_name, new_name)
            return True #nu a creat doar a modificat
        else:
            return False

        #codul 4.04 corespunde la una dintre cele 2 erori:
            #negasirea unui path valabil care sa contina old_name
            #incercarea redenumirii fisierului vechi cu un nume care este deja folosit(new_name)

def create_directory(dir_path):

    if os.path.isdir(dir_path):#daca exista deja
        print(f"'{dir_path}' is an existing directory.")
        return False

    try:
        os.makedirs(dir_path, exist_ok=True)  # previne eroare daca directorul exista deja
        print(f"Directory '{dir_path}' created successfully.")
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")

















