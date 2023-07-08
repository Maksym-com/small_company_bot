# Крок 1. Створити програму обліку працівників у компанії. Основні компоненти:
# Додати працівника,
# Видалити працівника,
# Переглянути список працівників,
# Змінити заробітну плату працівника.

employees = {
    "Vadim": {
        "salary": 600,
        "position": "Junior Python Developer",
        "start_date": "2023-05-07"
    },
    "Yaroslav": {
        "salary": 1500,
        "position": "Manager",
        "start_date": "2023-05-07"
    },
    "John": {
        "salary": 5000,
        "position": "CEO",
        "start_date": "2023-05-07"
    },
}

logs = {}

while True:
    user_command = input("Введіть команду (add, remove, view, change salary, change position, quit): ")
    if user_command == "add":

        while True:
            name = input("Напишіть ім'я:")
            if name in employees:
                user_command = input("Такий користувач вже існує, хочете перезаписати його інформацію? (так/ні): ")
                if user_command == "так":
                    break
                else:
                    print("Переходимо знову до вибору імені")
            else:
                break
        
        position = input("Напишіть позицію: ")
        salary = input("Напишіть зарплатню: ")
        start_date = input("Напишіть дату початку роботи: ")
        
        employees[name] = {
            "salary": salary,
            "position": position,
            "start_date": start_date
        }
    elif user_command == "remove":
        name = input("Напишіть ім'я працівника якого бажаєте видалити: ")
        
        if name in employees:
            del employees[name]
        else:
            print("Такого працівника немає")
            continue
    
    elif user_command == "view":
        print(f"{'Name':<15}{'Salary (USD)':<20}{'Position':20}{'Started to work':>20}")

        for name in employees:
            print("-" * 80)
            print(f"{name:<15}{employees[name]['salary']:<20}{employees[name]['position']:20}{employees[name]['start_date']:>20}")
            # зробити це у вигляді красивої таблички (зверху іменування колонок, а далі в циклі у них будуть значення)
            # Невдалий приклад, можете його модифікувати щоб покращити!
        print("-" * 80)
        continue
    elif user_command == "change salary":
        name = input("Напишіть ім'я працівника якому змінимо зарплатню: ")
        if name in employees:
            print(f"Наразі {name} заробляє - {employees[name]['salary']}")
        else:
            print("Такого працівника немає")
            continue
        
        new_salary = int(input("Введіть нову зарплатню: "))
        employees[name]["salary"] = new_salary
        print(f"Успішно змінено! {name} заробляє - {employees[name]['salary']}")

    elif user_command == "change position":
        name = input("Напишіть ім'я працівника якому змінимо посаду: ")
        if name in employees:
            print(f"Наразі {name} - {employees[name]['position']}")
        else:
            print("Такого працівника немає")
            continue
        
        new_position = (input("Введіть нову посаду: "))
        employees[name]["position"] = new_position
        print(f"Успішно змінено! Тепер {name} - {employees[name]['position']}")

    elif user_command == "quit":
        print("Вихід з програми....")
        break
    else:
        print("Невідома команда")

# Зробити вигляді красивої таблички (зверху іменування колонок, а далі в циклі у них будуть значення)
# Додати функціонал зміни позиції працівника. (команда 'change position')