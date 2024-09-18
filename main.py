import sql_func

def main(choice):
    match choice:
        case '1':
            sql_func.ex_1()
        case '2':
            sql_func.ex_2()
        case '3':
            sql_func.ex_3()
        case '4':
            sql_func.ex_4()
        case '5':
            sql_func.ex_5()
        case '6':
            sql_func.ex_6()
        case '7':
            sql_func.ex_7()
        case '8':
            sql_func.ex_8()
        case '9':
            sql_func.ex_9()
        case '10':
            sql_func.ex_10()  
        case '11':
            sql_func.ex_11()
        case '12':
            sql_func.ex_12()
        case 'exit':
            print("Exiting program.")
            return False
        case _:
            print("Invalid choice. Please enter a number between 1 and 12 or 'exit'.\n")
    return True

if __name__ == '__main__':
    while True:
        choice = input("Choose the exercise in range from 1 - 12: (e.g. '7') or 'exit': ").strip()
        
        # Call the main function and break the loop if it returns False
        if not main(choice):
            break
