import requests
import sys
import json

# library to enable printing formatted tables to the terminal
from rich.console import Console
from rich.table import Table

# initialize console to be able to print in formatted tables
console = Console()


# main function that runs the program
def run():
    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )
    print("                                  Welcome to this revision page")
    print("                                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("We hope this will help you gain mastery of Python, JavaScript and MySQL.")
    print(
        "On this page you can find a list of questions about Python, JavaScript and MySQL - you can answer these"
    )
    print(
        "questions and as you learn raise your mastery level - from the beginner 0 to a high level 10. "
    )
    print(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )
    print()
    print("To begin select from the following options")
    print()
    while True:

        print("Press 1 to display all the available questions and answers")
        print("Press 2 to select questions by language (Python, JavaScript or MySQL")
        print("Press 3 to add your own question and help other learners")
        print("Press 4 to find a question using the id number")
        print("Press 5 to delete a question incase you want to remove a question")
        print(
            "Press 6 to update your mastery level - your mastery level starts at zero - but work hard and reach 10"
        )
        print()
        #  ask user for their choice
        selection = get_choice(input("Please make your choice: ").strip())
        print()
        # run corresponding function based on their choice
        match selection:
            case 1:
                display_all_questions()
            case 2:
                get_question_by_language()
            case 3:
                add_own_question()
            case 4:
                get_question_by_id()
            case 5:
                delete_question()
            case 6:
                update_mastery()
        # ask user if they want to make another choice
        more_practice = (
            input("Would you like to contintue and practice more?(Y/N): ")
            .strip()
            .lower()
        )
        # based on their choice, either continue or exit the program
        run_again(more_practice)


# function that runs the program again or exits
def run_again(more_practice):
    # if yes, return true (to continue)
    if more_practice in ["y", "yes"]:
        return True
    # if no, exit the program
    elif more_practice in ["n", "no"]:
        print()
        sys.exit("Thank you for using our revision app.")
    # if invalid input (anything else other than y/yes, n/no), re-prompt the user
    else:
        return run_again(
            input(
                "Invalid entry. Please only enter y/yes to keep practicing or n/no to exit the program. "
            )
            .strip()
            .lower()
        )


# get a valid choice from user
def get_choice(choice):
    # if yes, return true (to continue)
    try:
        choice = int(choice)
        if 1 <= choice <= 6:
            return choice
        # if invalid input (anything else other than 1-6), re-prompt the user
        else:
            return get_choice(
                input(
                    "Incorrect choice, please try again (select number 1 - 6.): "
                ).strip()
            )
    # if string is entered that can't be convered into an int, ValueError is raised
    except ValueError:
        return get_choice(
            input("Incorrect choice, please try again (select number 1 - 6.): ").strip()
        )


# get and display all the questions from the API
def display_all_questions():
    # make API call to get all questions
    url = "http://127.0.0.1:5000/questions"
    headers = {"Content-Type": "application/json"}
    result = requests.get(url, headers)
    result_json = result.json()

    if result.status_code == 200:
        # display result in a formatted table (using rich library)
        table = Table(title="Revision questions", show_lines=True)
        # set the headers
        table.add_column("Question id", width=10)
        table.add_column("Programming Language", width=15)
        table.add_column("Question", width=30)
        table.add_column("Answer", width=30)
        table.add_column("Mastery Level", width=10)
        # add columns
        for each in result_json:
            table.add_row(
                str(each["question_id"]),
                each["programming_language"],
                each["question"],
                each["answer"],
                str(each["mastery_level_0_to_10"]),
            )
        # print table
        console.print(table)
    else:
        # if unsuccessful, let the user know
        print("Question ID not found.", result_json["error"])


# create own question and add to the API
def add_own_question():
    # ask user for proramming language, question and answer
    language = input("Please enter programming language: ").strip()
    question = input("Please enter your question: ").strip()
    answer = input("Please enter the answer to this question: ").strip()
    # create new question dictionary
    new_question = {
        key: value
        for key, value in {
            ("language", language),
            ("question", question),
            ("answer", answer),
        }
        if value
    }
    # make a post request to the API
    url = "http://127.0.0.1:5000/questions"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(new_question), headers=headers)

    # if response ok, confirm the question has been created and display the question
    if response.status_code == 201:
        created_question = response.json()
        print()
        # create table, columns and row
        table = Table(title="New question created successfully.", show_lines=True)
        table.add_column("Question id", width=10)
        table.add_column("Programming Language", width=15)
        table.add_column("Question", width=30)
        table.add_column("Answer", width=30)
        table.add_column("Mastery Level", width=10)
        table.add_row(
            str(created_question["question_id"]),
            created_question["programming_language"],
            created_question["question"],
            created_question["answer"],
            str(created_question["mastery_level_0_to_10"]),
        )
        # display the table
        console.print(table)
    else:
        # if post request unsuccessful, let the user know
        error_message = response.json()
        print("Failed to create question.", error_message["error"])


def get_number(choice):
    try:
        choice = int(choice)
        return choice
    # if string is entered that can't be convered into an int, ValueError is raised
    except ValueError:
        return get_number(
            input("Incorrect choice, please enter a number: ").strip()
        )


# delete question from API
def delete_question():
    # ask user for the question id they with to delete
    id_choice = input("Please enter question number (id) you wish to delete: ").strip()
    id_to_delete = get_number(id_choice)
    # make a delete request to the API
    url = f"http://127.0.0.1:5000/questions/{id_to_delete}"
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    response_json = response.json()
    # if response ok, confirm the question has been deleted
    if response.status_code == 200:
        print(f"Question number {id_to_delete} deleted successfully.")
    else:
        # if delete request unsuccessful, let the user know
        print("Unable to delete question.", response_json["error"])


# update mastery level
def update_mastery():
    # ask user for the question id they with to update the mastery for
    id_choice = input("Enter question id you wish to update the mastery for: ").strip()
    id = get_number(id_choice)
    mastery_choice = input("Enter mastery level (0-10): ").strip()
    mastery_level = get_number(mastery_choice)
    # make a PATCH request
    url = f"http://127.0.0.1:5000/questions/{id}"
    mastery = {"mastery": mastery_level}
    headers = {"Content-Type": "application/json"}
    response = requests.patch(url, data=json.dumps(mastery), headers=headers)
    response_json = response.json()
    # if response ok, confirm the mastery has been updated and show the updated record
    if response.status_code == 200:
        print()
        update = response_json["update"]
        table = Table(title="Mastery updated successfully.", show_lines=True)
        table.add_column("Question id", width=10)
        table.add_column("Programming Language", width=15)
        table.add_column("Question", width=30)
        table.add_column("Answer", width=30)
        table.add_column("Mastery Level", width=10)
        table.add_row(
            str(update["question_id"]),
            update["programming_language"],
            update["question"],
            update["answer"],
            str(update["mastery_level_0_to_10"]),
        )
        console.print(table)
    else:
        # if update unsuccessful, let the user know
        print("Failed to update mastery.", response_json["error"])


# get and display question based on requested id
def get_question_by_id():
    # ask the user for the question id they want to return
    id_choice = input("Please enter the question id number you want to see: ").strip()
    id_to_return = get_number(id_choice)
    # make a get request from the API
    url = f"http://127.0.0.1:5000/questions/{id_to_return}"
    headers = {"Content-Type": "application/json"}
    results = requests.get(url, headers)
    result_json = results.json()
    # if response is ok, return the question
    if results.status_code == 200:
        # display result in a formatted table (using rich library)
        table = Table(title="Revision questions", show_lines=True)
        # set the headers
        table.add_column("Question id", width=10)
        table.add_column("Programming Language", width=15)
        table.add_column("Question", width=30)
        table.add_column("Answer", width=30)
        table.add_column("Mastery Level", width=10)
        # add rows
        table.add_row(
            str(result_json[0]["question_id"]),
            result_json[0]["programming_language"],
            result_json[0]["question"],
            result_json[0]["answer"],
            str(result_json[0]["mastery_level_0_to_10"]),
        )
        # print table
        console.print(table)
    else:
        # if unsuccessful, let the user know
        print("Question ID not found.", result_json["error"])


def get_question_by_language():
    # ask the user for the question id they want to return
    language_to_return = input(
        "Please enter the programming language you want to see: "
    ).strip()

    # make a get request from the API
    url = f"http://127.0.0.1:5000/questions/language/{language_to_return}"
    headers = {"Content-Type": "application/json"}
    results = requests.get(url, headers)
    result_json = results.json()
    # if response is ok, return the questions
    if results.status_code == 200:
        # display result in a formatted table (using rich library)
        table = Table(title="Revision questions", show_lines=True)
        # set the headers
        table.add_column("Question id", width=10)
        table.add_column("Programming Language", width=15)
        table.add_column("Question", width=30)
        table.add_column("Answer", width=30)
        table.add_column("Mastery Level", width=10)
        # add rows
        for each in result_json:
            table.add_row(
                str(each["question_id"]),
                each["programming_language"],
                each["question"],
                each["answer"],
                str(each["mastery_level_0_to_10"]),
            )
        # print table
        console.print(table)
    else:
        # if unsuccessful, let the user know
        print("Programming language not found.", result_json["error"])


if __name__ == "__main__":
    run()
