import pytest
import requests
import mysql.connector  # type: ignore
import json

def add_item_to_db(item_id, item_description, item_completed):
    connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
    cursor = connection.cursor()
    query = "INSERT INTO items " "(item_id, description, completed)" "VALUES (%s, %s, %s)"
    cursor.execute(query, (item_id, item_description, item_completed))
    connection.commit()
    cursor.close()

@pytest.fixture(autouse=True)
def clear_db():
    yield None
    connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
    cursor = connection.cursor()
    query = "DELETE FROM items"
    cursor.execute(query)
    connection.commit()
    cursor.close()

def test_fetch_items():
    # GIVEN
    item_id = "SOME_ID"
    description = "SOME_DESCRIPTION"
    completed = 0
    add_item_to_db(item_id, description, completed)

    # WHEN 
    session = requests.Session()
    headers = {'Content-Type': 'application/json'}
    data = {"user_identifier": "1"}
    response = session.post('http://todo_app:5001/fetch-items', headers=headers, data=json.dumps(data))
    response_obj = json.loads(response.json())
    item = response_obj["items"][0]

    # THEN
    assert len(response_obj["items"]) == 1
    assert item["item_id"] == item_id
    assert item["message"] == description
    assert item["checked"] == completed