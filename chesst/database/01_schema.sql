DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS move;
DROP TABLE IF EXISTS comment;

CREATE TABLE player (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(128) UNIQUE,
  password VARCHAR(128),
  first_name VARCHAR(128),
  last_name VARCHAR(128)
);

CREATE TABLE game (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(128),
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  player_white INTEGER NOT NULL,
  player_black INTEGER NOT NULL,
  played_on TIMESTAMP NOT NULL,
  FOREIGN KEY (author_id) REFERENCES player (id)
  FOREIGN KEY (player_white) REFERENCES player (id)
  FOREIGN KEY (player_black) REFERENCES player (id)
);

CREATE TABLE move (
    game_id INTEGER,
    number INTEGER,
    notation VARCHAR(6),
    PRIMARY KEY(game_id, number)
);

CREATE TABLE comment (
    game_id INTEGER,
    move_number INTEGER,
    number INTEGER,
    player_id INTEGER,
    PRIMARY KEY(game_id, move_number, number),
    FOREIGN KEY (player_id) REFERENCES player (id)
)
