-- 3.a Afficher réservations avec nom client et ville hôtel
SELECT r.id AS reservation_id, c.nom AS client_nom, h.ville AS hotel_ville
FROM Reservation r
JOIN Client c ON r.client_id = c.id
JOIN Chambre ch ON r.chambre_id = ch.id
JOIN Hotel h ON ch.hotel_id = h.id;

-- 3.b Afficher les clients qui habitent à Paris
SELECT * FROM Client
WHERE ville = 'Paris';

-- 3.c Nombre de réservations par client
SELECT c.nom AS client_nom, COUNT(r.id) AS nb_reservations
FROM Client c
LEFT JOIN Reservation r ON c.id = r.client_id
GROUP BY c.nom;

-- 3.d Nombre de chambres par type
SELECT tc.nom AS type_chambre, COUNT(c.id) AS nb_chambres
FROM TypeChambre tc
JOIN Chambre c ON c.type_id = tc.id
GROUP BY tc.nom;

-- 3.e Chambres non réservées pendant une période (ex. août 2025)
SELECT *
FROM Chambre
WHERE id NOT IN (
    SELECT chambre_id
    FROM Reservation
    WHERE NOT (
        date_fin < '2025-08-01' OR date_debut > '2025-08-10'
    )
);
