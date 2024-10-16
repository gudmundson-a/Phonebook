class Contact:                                          #Klass för att skapa kontakter som lagrar info om namn, nummer och eventuella alias
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.aliases = []                               #Eventuella alias lagras i denna lista

                                                        #Metoden för att kunna lägga till eventuella alias till kontakten
    def add_alias(self, alias):
        self.aliases.append(alias)

                                                        #Funktion för att lägga till ny kontakt
def add_contact(phonebook, name, number):
    if name in phonebook:                               #Letar efter namn som nyckel i phonebook, om det redan finns skrivs felmeddelande ut
        print(f"{name} already exists.")                #Loopar igenom och kollar alla nummer i telefonboken ifall det man försöker lägga till redan finns.
    elif any(contact.number == number for contact in phonebook.values()):
        print(f"{number} already exists.")              #Här används .values() för att leta i värden och inte bara nycklar.
    else:
        phonebook[name] = Contact(name, number)         #Lägger till i phonebook med namn som nyckel, objektet som värde


def lookup(phonebook, name):
    contact = phonebook.get(name)                       #Kollar upp kontaktobjektet i telefonboken, använder namn som nyckel
    if contact:
        print(f"{name}: {contact.number}")              #Hittas kontakten skrivs information ut
    else:
        print(f"{name} not found.")


def assign_alias(phonebook, name, alias):
    contact = phonebook.get(name)
    if contact:
        if alias in phonebook:
            print(f"{alias} already exists.")
        else:
            contact.add_alias(alias)
            phonebook[alias] = contact                  #lägger till alias till en kontakt, alias blir nyckeln (Denna pekar alltså på en befintlig kontakt)
            print(f"Alias {alias} added for {name}.")
    else:
        print(f"Name not found or duplicate name")


def change_number(phonebook, name, new_number):
    contact = phonebook.get(name)
    if contact:                                         #Om numret användaren försöker lägga in ett telefonnummer som någon av kontakterna redan har blir bytet blockerat.
        if any(c.number == new_number for c in phonebook.values()):
            print(f"{new_number} already exists.")
        else:
            contact.number = new_number                 #Fanns inte det nya numret i någon kontakt så uppdateras numret.
            print(f"{name}'s new number is now {new_number}.")
    else:
        print(f"{name} not found.")


def save_file(phonebook, filename):
    saved = set()                                       #Lagrar namn och alias som skrivits till filen så att det ej blir dubletter. (set() constructor)
    with open(filename, 'w') as f:                      #Öppnar filen som ett filobjekt så att det går att skriva till filen
        for name, contact in phonebook.items():         #loopar igenom alla objekt i dictionaryn med namn som nyckelvärde och contact som objekt
            if name not in saved:                       #Kollar så att namnet inte redan finns i filen, om det ej finns skrivs det till filen
                f.write(f"{contact.number};{name};\n")
                saved.add(name)

            for alias in contact.aliases:               #Gör samma som delen för namn, fast nu med alias.
                if alias not in saved:
                    f.write(f"{contact.number};{alias};\n")
                    saved.add(alias)
    print(f"Phonebook saved to {filename}.")


def load_phonebook(phonebook, filename):
    phonebook.clear()                                   #Rensar det som eventuellt finns i phonebook för att ersätta med innehåll från filen du laddar in.
    try:                                                #Försök öppna fil med read, kolla varje rad i filen och hämta nummer och namn
        with open(filename, 'r') as f:
            for line in f:                              #På varje linje eventuella whitespaces bort
                line = line.strip()
                if not line:
                    continue

                parts = line.split(';')                 #Delar upp varje rad i nummer och namn, skapar ett Contact-objekt från dessa delar.

                if len(parts) < 2:                      #har "parts" för få delar kommer den inte kunna läggas till som ett objekt och skippas därför.
                    print(f"Skipping invalid line: {line}.")
                    continue

                number, name = parts[0], parts[1]

                if name not in phonebook:               #Så länge namnet inte redan fanns i phonebook så kommer det att läggas till som en ny kontakt
                    phonebook[name] = Contact(name, number)
        print(f"Phonebook loaded from {filename}.")
    except FileNotFoundError:                           #Hanterar eventuella fel där användaren letat efter fil som ej finns.
        print(f"File {filename} not found.")
    return phonebook                                    #Skickar phonebook tillbaka så att den går att använda i main.

def help():                                             #En funktion som hjälper användaren förstå vilka kommandon som finns
    print(f"\nAvailable commands: ")
    print(f" add (name, number)\n alias (name, newname)\n lookup (name)\n change (number, newnumber)\n save (filename)\n load (filename)\n quit\n{('-' *20)}")


def main():                                             #Skapar ett dictionary för att lagra contact-objekten.
    phonebook = {}                                      #Tar input från användaren och plockar bort whitespaces och separerar rader.

    while True:
        command = input("phoneBook> ").split()         #Tar bort whitespaces från input & gör att varje "ord" i strängen blir separat.
                                                       #Lagrar temporärt varje "ord" i en lista som sedan kommer kunna användas på ett objekt. (Contacts, i detta fall)
        if not command:
            continue

        cmd = command[0].lower()                        #Ser till att första kommandot blir lowercase så att man inte får fel om användaren råkar skriva tex "Add".

        if cmd == "add" and len(command) == 3:          #Kollar vad första delen i listan är, stämmer det överrens med "add" och även längden på den temporära listan är korrekt
            name, number = command[1], command[2]       #kommer namn och nummer bli tilldelat plats 1 och 2 i listan. Detta läggs sedan till i contacts med hjälp av add_contact funktionen.
            add_contact(phonebook, name, number)

        elif cmd == "alias" and len(command) == 3:      #Här och framöver gäller samma som ovan fast för andra ord, tex "alias, lookup osv.."
            name, alias = command[1], command[2]
            assign_alias(phonebook, name, alias)

        elif cmd == "lookup" and len(command) == 2:
            name = command[1]
            lookup(phonebook, name)

        elif cmd == "change" and len(command) == 3:
            name, new_number = command[1], command[2]
            change_number(phonebook, name, new_number)

        elif cmd == "save" and len(command) == 2:
            filename = command[1]
            save_file(phonebook, filename)

        elif cmd == "load" and len(command) == 2:
            filename = command[1]
            load_phonebook(phonebook, filename)

        elif cmd == "quit":
            print("Exiting phonebook...")
            break

        elif cmd == "help":
            help()

        else:
            print("Invalid command or wrong number of arguments.")

main()