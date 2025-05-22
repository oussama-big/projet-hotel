-- Création de la table Hotel

CREATE TABLE Hotel (
    id INT PRIMARY KEY,
    ville VARCHAR(50),
    pays VARCHAR(50),
    code_postal INT
);

-- Création de la table Client
CREATE TABLE Client (
    id INT PRIMARY KEY,
    adresse VARCHAR(100),
    ville VARCHAR(50),
    code_postal INT,
    email VARCHAR(100),
    telephone VARCHAR(20),
    nom VARCHAR(100)
);

-- Création de la table Prestation
CREATE TABLE Prestation (
    id INT PRIMARY KEY,
    prix DECIMAL(5,2),
    description VARCHAR(100)
);

-- Création de la table TypeChambre
CREATE TABLE TypeChambre (
    id INT PRIMARY KEY,
    nom VARCHAR(50),
    prix DECIMAL(6,2)
);

-- Création de la table Chambre
CREATE TABLE Chambre (
    id INT PRIMARY KEY,
    numero INT,
    etage INT,
    balcon BOOLEAN,
    type_id INT,
    hotel_id INT,
    FOREIGN KEY (type_id) REFERENCES TypeChambre(id),
    FOREIGN KEY (hotel_id) REFERENCES Hotel(id)
);

-- Création de la table Reservation
CREATE TABLE Reservation (
    id INT PRIMARY KEY,
    date_debut DATE,
    date_fin DATE,
    client_id INT,
    chambre_id INT,
    FOREIGN KEY (client_id) REFERENCES Client(id),
    FOREIGN KEY (chambre_id) REFERENCES Chambre(id)
);

-- Création de la table Evaluation
CREATE TABLE Evaluation (
    id INT PRIMARY KEY,
    date DATE,
    note INT CHECK (note BETWEEN 1 AND 5),
    commentaire TEXT,
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES Client(id)
);
