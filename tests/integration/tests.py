import pytest
import requests
import mysql.connector  # type: ignore
import json

# Helper funcs
def add_item_to_db(item_id, item_description, item_completed):
    connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
    cursor = connection.cursor()
    query = "INSERT INTO items " "(item_id, description, completed)" "VALUES (%s, %s, %s)"
    cursor.execute(query, (item_id, item_description, item_completed))
    connection.commit()
    cursor.close()


def get_all_items_from_db():
    connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = []
    for (item_id, description, completed) in cursor:  # type: ignore
        items.append({"item_id": item_id, "message": description, "checked": completed})
    connection.close()
    return items


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


# Tests
@pytest.mark.parametrize(
    "items",
    [
        ([{"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0}]),
        (
            [
                {"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0},
                {"item_id": "SOME_ID_1", "description": "SOME_DESCRIPTION_1", "completed": 1},
            ]
        ),
        (
            [
                {"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0},
                {"item_id": "SOME_ID_1", "description": "SOME_DESCRIPTION_1", "completed": 1},
                {"item_id": "SOME_ID_2", "description": "SOME_DESCRIPTION_2", "completed": 0},
            ]
        ),
    ],
)
def test_fetch_items_returns_all_items_in_db(items):
    # GIVEN
    for item in items:
        add_item_to_db(item["item_id"], item["description"], item["completed"])

    # WHEN
    session = requests.Session()
    headers = {"Content-Type": "application/json"}
    data = {"user_identifier": "1"}
    response = session.post("http://todo_app:5001/fetch-items", headers=headers, data=json.dumps(data))
    response_obj = json.loads(response.json())
    response_items = response_obj["items"]

    # THEN
    assert len(response_obj["items"]) == len(items)
    for input_item, response_item in zip(items, response_items):
        assert input_item["item_id"] == response_item["item_id"]
        assert input_item["description"] == response_item["message"]
        assert input_item["completed"] == response_item["checked"]


@pytest.mark.parametrize(
    "items, items_added",
    [
        ([{"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0}], 1),
        (
            [
                {"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0},
                {"item_id": "SOME_ID_1", "description": "SOME_DESCRIPTION_1", "completed": 1},
            ],
            2,
        ),
    ],
)
def test_add_item_succesfully_adds_item_to_db(items, items_added):
    # GIVEN
    items_in_db = get_all_items_from_db()
    assert len(items_in_db) == 0

    # WHEN
    session = requests.Session()
    headers = {"Content-Type": "application/json"}
    for item in items:
        data = {"item_id": item["item_id"], "message": item["description"], "checked": item["completed"]}
        response = session.post("http://todo_app:5001/add-item", headers=headers, data=json.dumps(data))

    # THEN
    items_in_db = get_all_items_from_db()
    # should probably loop through all items and check too
    assert len(items_in_db) == items_added


@pytest.mark.parametrize(
    "items",
    [
        ([{"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0}]),
        (
            [
                {"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0},
                {"item_id": "SOME_ID_1", "description": "SOME_DESCRIPTION_1", "completed": 1},
            ]
        ),
    ],
)
def test_check_item_succesfully_updates_correct_item_in_db(items):
    # GIVEN
    for item in items:
        add_item_to_db(item["item_id"], item["description"], item["completed"])

    # WHEN
    session = requests.Session()
    headers = {"Content-Type": "application/json"}
    for item in items:
        data = {"item_id": item["item_id"]}
        response = session.post("http://todo_app:5001/check-item", headers=headers, data=json.dumps(data))

    db_items = get_all_items_from_db()

    # THEN
    assert response.status_code == 200
    for item_added, item_in_db in zip(items, db_items):
        assert item_added["item_id"] == item_in_db["item_id"]
        assert item_added["completed"] == int(not bool(item_in_db["checked"]))


@pytest.mark.parametrize(
    "items, items_added",
    [
        ([{"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0}], 1),
        (
            [
                {"item_id": "SOME_ID", "description": "SOME_DESCRIPTION", "completed": 0},
                {"item_id": "SOME_ID_1", "description": "SOME_DESCRIPTION_1", "completed": 1},
            ],
            2,
        ),
    ],
)
def test_delete_item_succesfully_deletes_correct_item_in_db(items, items_added):
    # GIVEN
    for item in items:
        add_item_to_db(item["item_id"], item["description"], item["completed"])
    items_in_db = get_all_items_from_db()
    assert len(items_in_db) == items_added

    # WHEN
    session = requests.Session()
    headers = {"Content-Type": "application/json"}
    for item in items:
        data = {"item_id": item["item_id"]}
        response = session.post("http://todo_app:5001/delete-item", headers=headers, data=json.dumps(data))

    # THEN
    db_items = get_all_items_from_db()
    assert len(db_items) == 0


@pytest.mark.parametrize(
    "item",
    (
        [
            {"item_id": "", "description": "SOME_DESCRIPTION", "completed": 0},
            {"item_id": "SOME_ID", "description": "", "completed": 0},
            {"item_id": "", "description": "", "completed": 1},
        ]
    ),
)
def test_add_item_does_not_add_item_with_missing_id_or_description(item):
    # GIVEN
    items_in_db = get_all_items_from_db()
    assert len(items_in_db) == 0

    # WHEN
    session = requests.Session()
    headers = {"Content-Type": "application/json"}
    data = {"item_id": item["item_id"], "message": item["description"], "checked": item["completed"]}
    response = session.post("http://todo_app:5001/add-item", headers=headers, data=json.dumps(data))

    # THEN
    items_in_db = get_all_items_from_db()
    assert len(items_in_db) == 0
