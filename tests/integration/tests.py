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
    # test tear down
    connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
    cursor = connection.cursor()
    query = "DELETE FROM items"
    cursor.execute(query)
    connection.commit()
    cursor.close()

@pytest.mark.parametrize("items", [([{"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0}]),
                                   
                                   ([{"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0}, 
                                     {"item_id": "SOME_ID_1", "description": "SOME_DESCRIPTION_1", "completed": 1}]),

                                   ([{"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0}, 
                                     {"item_id": "SOME_ID_1", "description": "SOME_DESCRIPTION_1", "completed": 1},
                                     {"item_id": "SOME_ID_2", "description": "SOME_DESCRIPTION_2", "completed": 0}])
                                  ]
                        )
def test_fetch_items_returns_all_items_in_db(items):
    # GIVEN
    for item in items:
        add_item_to_db(item["item_id"], item["description"], item["completed"])

    # WHEN 
    session = requests.Session()
    headers = {'Content-Type': 'application/json'}
    data = {"user_identifier": "1"}
    response = session.post('http://todo_app:5001/fetch-items', headers=headers, data=json.dumps(data))
    response_obj = json.loads(response.json())
    response_items = response_obj["items"]

    # THEN
    assert len(response_obj["items"]) == len(items)
    for input_item, response_item in zip(items, response_items):
        assert input_item["item_id"] == response_item["item_id"]
        assert input_item["description"] == response_item["message"]
        assert input_item["completed"] == response_item["checked"]