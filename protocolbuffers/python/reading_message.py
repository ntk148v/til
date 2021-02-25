import addressbook_pb2
import sys

# Iterates though all people in the AddressBook and prints info about them
def list_people(address_book):
    for person in address_book.people:
        print("Person ID: ", person.id)
        print("* Name: ", person.name)
        if person.HasField("email"):
            print("* Email addres: ", person.email)

        for phone_number in person.phones:
            if phone_number.type == addressbook_pb2.Person.PhoneType.MOBILE:
                print("* Mobile phone: ")
            elif phone_number.type == addressbook_pb2.Person.PhoneType.HOME:
                print("* Home phone: ")
            elif phone_number.type == addressbook_pb2.Person.PhoneType.WORK:
                print("* Work phone: ")
            print(phone_number.number)
# reads the entire address book from a file and prints all
# information inside.
if len(sys.argv) != 2:
    print("Usage: ", sys.argv[0], "ADDRESS_BOOK_FILE")
    sys.exit(-1)

address_book = addressbook_pb2.AddressBook()

# Read the existing address book
f = open(sys.argv[1], 'rb')
address_book.ParseFromString(f.read())
f.close()

list_people(address_book)

