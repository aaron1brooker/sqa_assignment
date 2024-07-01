use db;

CREATE TABLE items(
    item_id varchar(100) NOT NULL,
    description varchar(100) NOT NULL,
    completed boolean DEFAULT 0,
    PRIMARY KEY (item_id)
);

INSERT INTO items(item_id, description, completed)
VALUES("item_id_1","Complete ADA assignment", 1);

INSERT INTO items(item_id, description, completed)
VALUES("item_id_2","Cook dinner", 0);