#gradebook guy
import statistics
import os

students = []

def add_student(id, name, math, science, sst, english):
    student= {
    "id": id,
    "name": name,
    "math": math,
    "science": science,
    "sst": sst,
    "english": english, 
    }
    students.append(student)
    return f"{student['name']} has been added to the students"
 

def remove_student(id_to_remove):

    for student in students :
        # we are finding the nigga to jek
        if student["id"] == id_to_remove:
           # we are removing the nigga
           students.remove(student)
        else:
           continue
    return None


#get mean for a given subject 
def mean(subject):
    total = 0
    for student in students:
        total = total + student[subject]
    mean = total / len(students)
    return mean

#get mode for a subject guy
def mode(subject):
    mode_list = []
    for student in students:
        mode_list.append(student[subject])
    mode = statistics.mode(mode_list)
    return mode

def max_mark(subject):
    list = []
    for student in students:
        list.append(student[subject])
    max_mark = max(list)
    return max_mark

def min_mark(subject):
    list = []
    for student in students:
        list.append(student[subject])
    min_mark = min(list)
    return min_mark
def edit_mark(id, subject, new_score):
    for student in students:
        #find the nigga
        if student["id"] == id:
            #find the subject
            if subject in student:
                #change the mark  
                student[subject] = new_score
                print(f"{student['name']}'s {subject} has been changed to {new_score}")
                return  
    print(f"Student with ID {id} or subject {subject} not found")
    return None

def display_gradebook():
    print("*_*_*_*_*_*_*_*_*_*_*GRADE BOOK_*_*_*_*_*_*_*_*_*_*_*_*_*_*")
    for student in students:
        print(f"_____________________________{student["name"]}_______________________________________")
        print(f"MATH: |{student["math"]}")
        print(f"SST:  |{student["sst"]}")
        print(f"SCI:  |{student["science"]}")
        print(f"ENG:  |{student["english"]}")
    return None




def print_menu():
    print("--------------------Menu--------------------")
    print("1 - Add student with marks")
    print("2 - Delete student, given an admin_no")
    print("3 - View statistics about the grades")
    print("4 - View student grades")
    print("5 - Edit student grades")
    print("6 - Print Gradebook")
    print("m - Print menu")
    print("c - Clear Screen")
    print("q - Quit system\n")

print(f"Welcome to students Gradebook\nBy".upper())


#Print menu for first time
print_menu()


while True:
    choice = input("\n--------------------\nEnter your choice\n")
    
    if choice == '1':
        name = input("Name: ")
        id = input("Admin_no: ")
        math = int(input("Maths: "))
        sst = int(input("SST: "))
        science = int(input("Science: "))
        english = int(input("English: "))
        add_student(id, name, math, science, sst, english)
        print(f"{name} has been added to the students with marks MTC: {math}, SST: {sst}, SCI:{science}, ENG: {english}")
        print(students)
        
    elif choice == '2':
        id = input("Enter student to delete Admin_no: ")
        remove_student(id)
        print(f"Student deleted with id: {id}")
        print(students)
    
    elif choice == '3':
        #Add Code give the following gradebook statistics
        print("*************MATH STATS*********************")
        print(f"Mean marks for Maths: {mean('math')}")
        print(f"Mode mark for Maths: {mode('math')}")
        print(f"Lowest mark for Maths: {min_mark('math')}")
        print(f"Highest mark for Maths: {max_mark('math')}")

        print("*************SST STATS*********************")
        print(f"Mean marks for SST: {mean('sst')}")
        print(f"Mode mark for SST: {mode('sst')}")
        print(f"Lowest mark for SST: {min_mark('sst')}")
        print(f"Highest mark for SST: {max_mark('sst')}")

        print("*************SCI STATS*********************")
        print(f"Mean marks for SCI: {mean('science')}")
        print(f"Mode mark for SCI: {mode('science')}")
        print(f"Lowest mark for SCI: {min_mark('science')}")
        print(f"Highest mark for SCI: {max_mark('science')}")

    elif choice == '4':
        id = input("Enter student Admin_no: ")
        for student in students:
            if student["id"] == id:
                print(student)
                break
        else:
            print(f"Student with Admin_no {id} not found")

    elif choice == '5':
        id = input("Enter student Admin_no: ")
        subject = input("Enter subject: ")
        new_score = int(input("Enter new score: "))
        edit_mark(id, subject, new_score)

    elif choice == '6':
        display_gradebook()

    elif choice == 'm':
        print_menu()
    
    elif choice == 'c':
        os.system('clear') #Only for windows
        
    elif choice == 'q':
        print('Bye bye')
        break

"Want to code like this???"
"For python tutoring call/ whatsapp +256784275243- Lwanga Caleb"