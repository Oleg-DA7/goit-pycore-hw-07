# Сутності:

# Field: Базовий клас для полів запису.
# Name: Клас для зберігання імені контакту. Обов'язкове поле. 
# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр). (PhoneNumber)
# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів. (Contact)
# AddressBook: Клас для зберігання та управління записами. (ContactList)

# Функціональність:
# AddressBook:Додавання записів.
# Пошук записів за іменем.
# Видалення записів за іменем.
# Record:Додавання телефонів.
# Видалення телефонів.
# Редагування телефонів.
# Пошук телефону.

import re
from decorators import error_decorator

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class PhoneNumber(Field):
    def __init__(self, phone_number):
        if re.fullmatch('[0-9]{10}', phone_number) != None:
            super().__init__(phone_number)
        else:
            print("Enter the correct phone number!")
    def __str__(self):
        return f'Phone number - {self.value}'
    
class ContactName(Field):
    def __init__(self, name):
        super().__init__(name)
    def __str__(self):
        return f'{self.value}'

class Contact():
    def __init__(self, args):
        self.name = ContactName(args[0])
        self.phones = []

    def __str__(self):        
        return f'Contact name: {self.name.value}, phones: {[p.value for p in self.phones]}'
    
    @error_decorator(default_result=None)    
    def add_phone(self, args): # Додавання телефонів до контакту
        for i in self.phones:
            if i.value == args[1]:
                print(f'This number {args[1]} already exist in contact: {self.name.value}') 
                return None
        self.phones.append(PhoneNumber(args[1]))

    @error_decorator(default_result=None)  
    def del_phone(self, args): # Видалення телефону у контакта
        found = False
        for i in self.phones:
            if i.phone == args[1]:
                found = True
                self.phones.remove(i)
                print(f'Number {args[1]} deleted in contact: {self.name.value}') 
        if not found:
            print(f'Number {args[1]} not found in contact: {self.name.value}') 
        return None
    
    @error_decorator(default_result=None)          
    def change_phone(self, args): # Редагування телефонів - зміна номеру на інший
        found = False
        for i in self.phones:
            if i.value == args[1]:
                found = True
                i.value = args[2]
                print(f'Phone number {args[1]} changed to {i.value} in contact: {self.name.value}') 
        if not found:
            print(f'Number {args[1]} not found in contact: {self.name.value}') 
        return None
    
    @error_decorator(default_result=None)  
    def find_phone(self, args): # Пошук телефону
        found = False
        for i in self.phones:
            if i.value == args[1]:
                found = True
        if found: 
            return f'{args[1]} found in contact: {self.name.value}'
        else: 
            return f'{args[1]} not found in contact: {self.name.value}'
            

class ContactList():
    def __init__(self):
        self.contacts = []    

    @error_decorator(default_result = None)
    def add_contact(self, contact):
        self.contacts.append(contact)
        return (f'{contact} added.')
    
    def all_contacts(self):
        for i in self.contacts: 
            print(f'{i}')

    @error_decorator(default_result = None)
    def get_contact(self, args): 
        name = args[0]
        result = None
        for i in self.contacts:
            if i.name.value == name: 
                result = i
        if result == None : print(f'Contact {name} not found !')
        return result

    @error_decorator(default_result = None)
    def del_contact(self, args): 
        found = False
        name = args[0]
        for i in self.contacts:
            if i.name.value == name: 
                found = True
                self.contacts.remove(i)
                print(f'Contact {name} deleted')
        if not found: print(f'Contact {name} not found !')

    @error_decorator(default_result=None)
    def change_contact(self, args):
        result = 'Contact not found'
        for i in self.contacts:
            if i.name.value == args[0]: 
                i.name.value = args[1]
                result = f'Contact updated to {i}'
        return result

@error_decorator(default_result=[None, None])
def parse_input(user_input):    
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    cl = ContactList()
    print("Welcome to the assistant bot!")
    while True:
         user_input = input("Enter a command: ")
         command, *args = parse_input(user_input)
         match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")

# ContactList command -------------------------------------
            case "del":                
                cl.del_contact(args)  
            case "add":
                c = Contact(args)
                if c != None:
                    print(cl.add_contact(c))  
            case "change":
                result = cl.change_contact(args)                 
                if result != None:
                    print(result)         
            case "find":
                result = cl.get_contact(args)                 
                if result != None:
                    print(result)   
            case "all":
                cl.all_contacts()           

# Contact command -----------------------------------------
            case "add_phone":
                c = cl.get_contact(args)
                if c != None:
                    c.add_phone(args)    
            case "del_phone":
                c = cl.get_contact(args)
                if c != None:
                    c.del_phone(args)     
            case "change_phone":
                c = cl.get_contact(args)
                if c != None:
                    c.change_phone(args)                                
            case "find_phone":
                c = cl.get_contact(args)
                if c != None:
                    print(c.find_phone(args))



if __name__ == "__main__":
    main()

