CREATE TABLE IF NOT EXISTS challenger_players(
    summonerID INT GENERATED ALWAYS AS IDENTITY,
    playerID CHAR(56) NOT NULL UNIQUE,
    summonerName VARCHAR(16) NOT NULL UNIQUE,
    CONSTRAINT pk_player PRIMARY KEY(summonerID)
);

CREATE TABLE IF NOT EXISTS topTen(
    summonerID INT NOT NULL,
    dateOfAchievement DATE,
    CONSTRAINT pk_top PRIMARY KEY(summonerID, dateOfAchievement),
    CONSTRAINT fk_topPlayer FOREIGN KEY(summonerID) REFERENCES challenger_players(summonerID)
);

CREATE TABLE IF NOT EXISTS champions(
    championID INT NOT NULL,
    championName VARCHAR(16) NOT NULL,
    championPrimaryType VARCHAR(16) NOT NULL,
    championSecondaryType VARCHAR(16),
    CONSTRAINT pk_champ PRIMARY KEY(championID)
);

CREATE TABLE IF NOT EXISTS games(
    gameKey INT GENERATED ALWAYS AS IDENTITY,
    gameID CHAR(11) NOT NULL UNIQUE,
    summonerID INT NOT NULL,
    championID INT NOT NULL,
    CONSTRAINT pk_game PRIMARY KEY(gameKey),
    CONSTRAINT fk_player FOREIGN KEY(summonerID) REFERENCES challenger_players(summonerID),
    CONSTRAINT fk_champion FOREIGN KEY(championID) REFERENCES champions(championID)
);