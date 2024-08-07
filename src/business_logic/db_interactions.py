import mysql.connector  # type: ignore
import logging

logger = logging.getLogger(__name__)


def add_item_to_db(item_id, item_description, item_completed) -> bool:
    if item_id == None or item_id == "":
        logger.warn("Unable to add item without item_id")
        return False

    if item_description == None or item_description == "":
        logger.warn("Unable to add item without description")
        return False

    try:
        connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
        logger.info("Sucessfully connected to DB in add_item_to_db")
        cursor = connection.cursor()
        query = "INSERT INTO items " "(item_id, description, completed)" "VALUES (%s, %s, %s)"
        cursor.execute(query, (item_id, item_description, item_completed))
        connection.commit()
    except:
        logger.error(f"Failed to add item to database with item_id: {item_id}")
        return False
    finally:
        cursor.close()
        logger.info("item_id {item_id} successfully entered into DB")
        return True


def get_all_items() -> list:
    try:
        connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
        logger.info("Sucessfully connected to DB in get_all_items")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items")
    except:
        logger.error(f"Failed to fetch items from DB")
        return []
    finally:
        items = []
        for (item_id, description, completed) in cursor:  # type: ignore
            items.append({"item_id": item_id, "message": description, "checked": completed})
        connection.close()
        return items


def delete_item_from_db(item_id) -> bool:
    try:
        connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
        logger.info("Sucessfully connected to DB in delete_item_from_db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE item_id = %s", [item_id])
        connection.commit()
    except:
        logger.error(f"Failed to delete item with item_id: {item_id} from DB")
        return False
    finally:
        connection.close()
        logger.info(f"Succesfully removed item with item_id: {item_id} from database")
        return True


def check_item_in_db(item_id) -> bool:
    try:
        connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
        logger.info("Sucessfully connected to DB in delete_item_from_db")
        cursor = connection.cursor()
        query = "UPDATE items SET completed = !completed WHERE item_id = %s"
        cursor.execute(query, [item_id])
        connection.commit()
    except:
        logger.error(f"Failed to update checked status of item with item_id: {item_id} in DB")
        return False
    finally:
        connection.close()
        logger.info(f"Succesfully updated item with item_id: {item_id}")
        return True
