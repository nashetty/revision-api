import mysql.connector
from config import USER, PASSWORD, HOST

db_name = "revision"


# create custom exception for db connection failure
class DbConnectionError(Exception):
    pass


# create custom exceptions for user related errors
class UserError(Exception):
    pass


# connect to database
def db_connect(db_name):
    try:
        # establish a session with MySQL server
        connection = mysql.connector.connect(
            host=HOST, user=USER, password=PASSWORD, database=db_name
        )
        print(f"Connection to {db_name} successful.")
        return connection
    except mysql.connector.Error as e:
        raise DbConnectionError(f"Failed to connect to database: {e}")


# print(db_connect(db_name))

# get all questions available in db as a list of dictionaries
def get_all_questions():
    # initialize connection as None to be able to handle it in the finally bloce
    # in case a DbConnectionError error is raised. Without this, the program was crashing
    # when db name was incorrect
    connection = None
    try:
        # connect to the db
        connection = db_connect(db_name)
        # create cursor and set to return data type as dictionary instead of default tuple
        cursor = connection.cursor(dictionary=True)
        # print(f"Connection to {db_name} successful.")
        # execute the required db operation
        query = """
                    SELECT
                        question_id,
                        programming_language,
                        question,
                        answer,
                        mastery_level_0_to_10
                    FROM
                        questions
                """
        cursor.execute(query)
        #  fetch all rows of a query result set and return a list of dictionaries
        result = cursor.fetchall()
    # raise an error is data could not be read
    except mysql.connector.Error as e:
        raise DbConnectionError(f"Failed to fetch questions from database: {e}")
    finally:
        # if connection was successdul, close it
        if connection is not None:
            connection.close()
            print(f"{db_name} connection closed successfully")
    # return the data
    return result


# get questions by language
def get_questions_by_language(language):
    # initialize connection as None to be able to handle it in 'finally' block
    connection = None
    try:
        # connect to the db
        connection = db_connect(db_name)
        # create cursor and set to return data type as dictionary instead of default tuple
        cursor = connection.cursor(dictionary=True)
        # print(f"Connection to {db_name} successful.")
        # execute the required db operation
        query = """
                    SELECT
                        question_id,
                        programming_language,
                        question,
                        answer,
                        mastery_level_0_to_10
                    FROM
                        questions
                    WHERE
                        programming_language = %s
                """
        # pass the 'language' as a parameter to the execute method in order
        # to sanitize the data and to protect query from SQL injection
        cursor.execute(query, [language])
        #  fetch all rows of a query result set and return a list of dictionaries
        result = cursor.fetchall()
        if not result:
            raise UserError(f"Required language {language} not in the database")
    # raise an error if data could not be read
    except mysql.connector.Error as e:
        raise DbConnectionError(f"Failed to fetch questions from database: {e}")
    finally:
        # if connection was successful, close it
        if connection is not None:
            connection.close()
            print(f"{db_name} connection closed successfully")
    # return result
    return result


# get question by id
def get_question_by_id(id):
    # initialize connection as None to be able to handle it in 'finally' block
    connection = None
    try:
        # connect to the db
        connection = db_connect(db_name)
        # create cursor and set to return data type as dictionary instead of default tuple
        cursor = connection.cursor(dictionary=True)
        # print(f"Connection to {db_name} successful.")
        # check if id exists in the db
        query = """
                    SELECT
                        question_id,
                        programming_language,
                        question,
                        answer,
                        mastery_level_0_to_10
                    FROM
                        questions
                    WHERE
                        question_id = %s
                """
        # pass the id to the execute method as parameter in order
        # to sanitize the data and protect query from SQL injection
        cursor.execute(query, [id])
        result = cursor.fetchall()
        if not result:
            raise UserError(f"Question with id {id}  does not exist")
    # raise an error if data could not be inserted
    except mysql.connector.Error as e:
        raise DbConnectionError(f"Failed to get question {id}: {e}")
    finally:
        # if connection was successful, close it
        if connection is not None:
            connection.close()
            print(f"{db_name} connection closed successfully")
    return result


# insert new question into the table
def create_new_question(new_question):
    # initialize connection as None to be able to handle it in 'finally' block
    connection = None
    try:
        # connect to the db
        connection = db_connect(db_name)
        # create cursor
        cursor = connection.cursor()
        # print(f"Connection to {db_name} successful.")
        # Validate the JSON payload
        if not new_question:
            raise UserError("No data provided")

        required_fields = ["language", "question", "answer"]
        for field in required_fields:
            if field not in new_question:
                raise UserError(f"Missing required field: {field}")
        # If validation passes, proceed to create the question
        query = """
                    INSERT INTO
                        questions (programming_language, question, answer)
                    VALUES
                        (%s, %s, %s)
                """
        params = (
            new_question["language"],
            new_question["question"],
            new_question["answer"],
        )
        # pass the language, question and answer as a parameters to the execute method in order
        # to sanitize the data and protect query from SQL injection
        cursor.execute(query, params)
        # get the new id
        inserted_id = cursor.lastrowid
        connection.commit()
        print("New question created successfully")
    # raise an error if data could not be inserted
    except mysql.connector.Error as e:
        raise DbConnectionError(f"Failed to insert the data: {e}")
    finally:
        # if connection was successful, close it
        if connection is not None:
            connection.close()
            print(f"{db_name} connection closed successfully")
    # return the inserted record
    return {
        "question_id": inserted_id,
        "programming_language": new_question["language"],
        "question": new_question["question"],
        "answer": new_question["answer"],
        "mastery_level_0_to_10": 0,
    }


# delete question by id
def delete_question_by_id(id):
    # initialize connection as None to be able to handle it in 'finally' block
    connection = None
    try:
        # connect to the db
        connection = db_connect(db_name)
        # create cursor
        cursor = connection.cursor()
        # print(f"Connection to {db_name} successful.")
        # check if id exists in the db
        find_id = """SELECT question_id FROM questions WHERE question_id = %s"""
        cursor.execute(find_id, [id])
        result = cursor.fetchall()
        if not result:
            raise UserError(f"Question with id {id} does not exist")
        query = """
                    DELETE FROM questions WHERE question_id = %s
                """
        # pass the id to the execute method as parameter in order
        # to sanitize the data and protect query from SQL injection
        cursor.execute(query, [id])
        connection.commit()
        print(f"Question with id {id} deleted successfully")
    # raise an error if data could not be inserted
    except mysql.connector.Error as e:
        raise DbConnectionError(f"Failed to delete the question: {e}")
    finally:
        # if connection was successful, close it
        if connection is not None:
            connection.close()
            print(f"{db_name} connection closed successfully")


# update mastery level
def update_mastery_by_id(id, mastery_level):
    # initialize connection as None to be able to handle it in 'finally' block
    connection = None
    try:
        # connect to the db
        connection = db_connect(db_name)
        # create cursor with return data type dict instead of tuple
        cursor = connection.cursor(dictionary=True)
        # print(f"Connection to {db_name} successful.")
        # check if id exists in the db
        find_id = """
                    SELECT
                        question_id,
                        programming_language,
                        question,
                        answer
                    FROM
                        questions
                    WHERE
                        question_id = %s
                """
        cursor.execute(find_id, [id])
        result = cursor.fetchall()
        if not result:
            raise UserError(f"Question with id {id} does not exist")
        if not (0 <= mastery_level <= 10):
            raise UserError("Mastery Level needs to be between 0 and 10")
        result[0]["mastery_level_0_to_10"] = mastery_level
        query = """
                    UPDATE questions
                    SET mastery_level_0_to_10 = %s
                    WHERE question_id = %s
                """
        # pass the id and mastery to the execute method as parameter in order
        # to sanitize the data and protect query from SQL injection
        cursor.execute(query, [mastery_level, id])
        connection.commit()
        print(f"Mastery level for question with id {id} updated successfully")
    # raise an error if data could not be inserted
    except mysql.connector.Error as e:
        raise DbConnectionError(
            f"Failed to update the mastery level for question {id}: {e}"
        )
    finally:
        # if connection was successful, close it
        if connection is not None:
            connection.close()
            print(f"{db_name} connection closed successfully")
    return result[0]


if __name__ == "__main__":
    print(db_connect(db_name))
    # print(get_all_questions())
    # print(get_questions_by_language("Python"))
    # print(get_question_by_id(1))
    # print(
    #     create_new_question(
    #         {"language": "JavaScript", "question": "test123", "answer": "test"}
    #     )
    # )
    # delete_question_by_id(17)
    # print(update_mastery_by_id(1, 5))
