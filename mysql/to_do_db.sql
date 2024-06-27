use db;

CREATE TABLE items(
    item_id int not null AUTO_INCREMENT,
    description varchar(100) NOT NULL,
    completed boolean NOT NULL,
    deleted boolean NOT NULL,
    PRIMARY KEY (item_id)
);

INSERT INTO items(description, completed, deleted)
VALUES("Complete ADA assignment", 0, 0);