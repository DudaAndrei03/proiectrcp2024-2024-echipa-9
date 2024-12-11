import os

from enum import Enum

class Methods(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

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

            #print(f"Created empty file in : {file_path}")
            #return True

        except OSError as error:
            print(f"Failed to create the empty file:{file_path} due to {error}")
            return False

def create_file_for_move(folder_path,content):
    try:
        with open (folder_path, 'w') as File:
            File.write(content)
            return True
    except OSError as error:
        print(f"Failed to create the file for the MOVE operation : {folder_path} due to {error}")

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


def read_file(folder_path,filename): # mergea inainte cu filename, am pus file_path la with open
    file_path = os.path.join(folder_path, filename)
    try:
        with open(file_path,'r') as file: #deschid in binar pt a putea trimite in retea->trebuie citit cu 'wb'
            content=file.read()
            return content
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return False

def read_file_for_internal_operations(folder_path,filename):
    file_path = os.path.join(folder_path, filename)
    try:
        with open(file_path,'r') as file: #deschid in binar pt a putea trimite in retea->trebuie citit cu 'wb'
            content=file.read()
            return content
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return False

def move_File(folder_path_old_location,folder_path_new_location):
    filename = os.path.basename(folder_path_old_location)
    directory = os.path.dirname(folder_path_old_location)

    content = read_file_for_internal_operations(directory,filename)
    print(content)

    folder_path_new_location += f"/{filename}"
    create_file_for_move(folder_path_new_location,content)
    #delete ulterior al fisierului din folder_path_old_location


def create_dir(path):
    os.mkdir(path,mode=0o777)


def generate_code(method,content):
    code=None
    method_enum = Methods(method)

    if method_enum == Methods.GET:
        if content: #succes
            code = codeToDecimal('2.05')
        else:
            code = codeToDecimal('4.04')
    if method_enum == Methods.POST:
        if content:
            code = codeToDecimal('2.04')
        else:
            code = codeToDecimal('4.04')
    if method_enum == Methods.PUT:
        if content:
            code = codeToDecimal('2.04') #creat
        else:
            code= codeToDecimal('4.04')
    return code


def codeToDecimal(value: str) -> int:
    integer_part, fractional_part = value.split('.')

    # Convertim partea întreagă în întreg
    integer_value = int(integer_part)

    # Convertim partea fracționară în întreg
    fractional_value = int(fractional_part)

    # Obținem reprezentarea binară pe 3 biți pentru partea întreagă
    integer_binary = format(integer_value, '03b')

    # Obținem reprezentarea binară pe 5 biți pentru partea fracționară
    fractional_binary = format(fractional_value, '05b')

    # Combinăm cele două reprezentări binare
    combined_binary = integer_binary + fractional_binary

    # Convertim combinația din binar în decimal
    decimal_value = int(combined_binary, 2)

    return decimal_value


# Exemplu de utilizare
result = codeToDecimal("2.05")
print(result)  # Ar trebui să afișeze 69



def rename_file(folder_path,old_name, new_name):
        # Check if the source file exists
        old_name_path = os.path.join(folder_path,old_name)
        if not os.path.exists(old_name_path):
            return False

        # Check if the destination file already exists
        new_name_path=os.path.join(folder_path,new_name)
        if os.path.exists(new_name_path) == False:
            os.rename(old_name_path, new_name_path)
            return True #nu a creat doar a modificat
        else:
            return False

        #codul 4.04 corespunde la una dintre cele 2 erori:
            #negasirea unui path valabil care sa contina old_name
            #incercarea redenumirii fisierului vechi cu un nume care este deja folosit(new_name)

def create_directory(folder_path,dir_name):
    dir_full_path = os.path.join(folder_path,dir_name)

    if os.path.isdir(dir_full_path):#daca exista deja
        print(f"'{dir_full_path}' is an existing directory.")
        return False

    try:
        os.makedirs(dir_full_path, exist_ok=True)  # previne eroare daca directorul exista deja
        print(f"Directory '{dir_full_path}' created successfully.")
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")

















