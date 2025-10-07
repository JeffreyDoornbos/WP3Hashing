-- [normal_query]
SELECT onderzoeken.id, onderzoeken.titel, onderzoeken.beschikbaar, onderzoeken.locatie, GROUP_CONCAT(beperkingen.naam, ', '), onderzoeken.doelgroep_leeftijd_start, onderzoeken.doelgroep_leeftijd_eind, onderzoeken.met_beloning, onderzoeken.beloning, onderzoeken.start_datum, onderzoeken.eind_datum FROM onderzoeken
LEFT JOIN onderzoek_beperkingen ON onderzoeken.id = onderzoek_beperkingen.onderzoek_id
LEFT JOIN beperkingen ON onderzoek_beperkingen.beperking_id = beperkingen.id
WHERE onderzoeken.status_id=1
GROUP BY onderzoeken.id;

-- [count_query]
SELECT COUNT(*) FROM onderzoeken WHERE 1=1;

-- [doelgroep_query]
SELECT id, naam FROM beperkingen;


-- // Ophalen gegevens //
-- [get_onderzoek]
SELECT onderzoeken.id, onderzoeken.titel, onderzoeken.beschrijving, onderzoeken.beschikbaar, onderzoeken.locatie, GROUP_CONCAT(beperkingen.naam, ', '), onderzoeken.doelgroep_leeftijd_start, onderzoeken.doelgroep_leeftijd_eind, onderzoeken.met_beloning, onderzoeken.beloning, onderzoeken.start_datum, onderzoeken.eind_datum FROM onderzoeken
LEFT JOIN onderzoek_beperkingen ON onderzoeken.id = onderzoek_beperkingen.onderzoek_id
LEFT JOIN beperkingen ON onderzoek_beperkingen.beperking_id = beperkingen.id
WHERE onderzoeken.status_id=1 AND onderzoeken.id = ?
GROUP BY onderzoeken.id;

-- [test_gebruiker]
SELECT * FROM ervaringsdeskundigen WHERE id = 3;

-- [counting_query]
SELECT COUNT(DISTINCT onderzoeken.id) FROM onderzoeken
JOIN deelnamen ON onderzoeken.id = deelnamen.onderzoek_id
WHERE deelnamen.ervaringsdeskundige_id = ?;

-- [counting_doelgroep]
SELECT COUNT(DISTINCT onderzoeken.id) FROM onderzoeken
LEFT JOIN onderzoek_beperkingen ON onderzoeken.id = onderzoek_beperkingen.onderzoek_id
WHERE onderzoeken.status_id = 1
  AND onderzoek_beperkingen.beperking_id IN (
      SELECT beperking_id FROM ervaringsdeskundigen_beperkingen WHERE ervaringsdeskundige_id = ?
);

-- [deelnames]
SELECT
    onderzoeken.id,
    onderzoeken.titel,
    onderzoeken.beschikbaar,
    onderzoeken.locatie,
    GROUP_CONCAT(beperkingen.naam, ', ') AS beperkingen,
    onderzoeken.doelgroep_leeftijd_start,
    onderzoeken.doelgroep_leeftijd_eind,
    onderzoeken.met_beloning,
    onderzoeken.beloning,
    onderzoeken.start_datum,
    onderzoeken.eind_datum
FROM onderzoeken
JOIN deelnamen ON onderzoeken.id = deelnamen.onderzoek_id
LEFT JOIN onderzoek_beperkingen ON onderzoeken.id = onderzoek_beperkingen.onderzoek_id
LEFT JOIN beperkingen ON onderzoek_beperkingen.beperking_id = beperkingen.id
WHERE deelnamen.ervaringsdeskundige_id = ?
GROUP BY onderzoeken.id;

-- [doelgroepen]
SELECT
    onderzoeken.id,
    onderzoeken.titel,
    onderzoeken.beschikbaar,
    onderzoeken.locatie,
    GROUP_CONCAT(DISTINCT beperkingen.naam) AS beperkingen,
    onderzoeken.doelgroep_leeftijd_start,
    onderzoeken.doelgroep_leeftijd_eind,
    onderzoeken.met_beloning,
    onderzoeken.beloning,
    onderzoeken.start_datum,
    onderzoeken.eind_datum
FROM onderzoeken
LEFT JOIN onderzoek_beperkingen ON onderzoeken.id = onderzoek_beperkingen.onderzoek_id
LEFT JOIN beperkingen ON onderzoek_beperkingen.beperking_id = beperkingen.id
WHERE onderzoeken.status_id = 1
  AND beperkingen.id IN (
        SELECT beperking_id FROM ervaringsdeskundigen_beperkingen
        WHERE ervaringsdeskundige_id = ?
  )
GROUP BY onderzoeken.id;

-- [check_deelname]
SELECT onderzoek_id FROM deelnamen WHERE ervaringsdeskundige_id = ?;

-- [check_user]
SELECT * FROM ervaringsdeskundigen WHERE id = ?;

-- [eigen_doelgroepen]
SELECT beperkingen.id, beperkingen.naam
FROM beperkingen
JOIN ervaringsdeskundigen_beperkingen ON beperkingen.id = ervaringsdeskundigen_beperkingen.beperking_id
WHERE ervaringsdeskundigen_beperkingen.ervaringsdeskundige_id = ?;

-- [inschrijven]
INSERT INTO deelnamen (naam, datum, ervaringsdeskundige_id, onderzoek_id, status_id) VALUES (?,CURRENT_TIMESTAMP, ?, ?,3);

-- [uitschrijven]
DELETE FROM deelnamen WHERE ervaringsdeskundige_id = ? AND onderzoek_id = ?;

-- [profiel]
SELECT ervaringsdeskundigen.id, ervaringsdeskundigen.voornaam, ervaringsdeskundigen.achternaam, ervaringsdeskundigen.email, ervaringsdeskundigen.telefoonnr, ervaringsdeskundigen.geslacht, ervaringsdeskundigen.geboorte_datum, GROUP_CONCAT(beperkingen.naam, ', ') AS beperkingen, ervaringsdeskundigen.bijzonderheden, ervaringsdeskundigen.toezichthouder_id, ervaringsdeskundigen.bijzonderheden_beschikbaarheid, ervaringsdeskundigen.kort_voorstellen
FROM ervaringsdeskundigen
LEFT JOIN ervaringsdeskundigen_beperkingen ON ervaringsdeskundigen.id = ervaringsdeskundigen_beperkingen.ervaringsdeskundige_id
LEFT JOIN beperkingen ON ervaringsdeskundigen_beperkingen.beperking_id = beperkingen.id
WHERE ervaringsdeskundigen.id = ?
GROUP BY ervaringsdeskundigen.id;

-- [update]
UPDATE ervaringsdeskundigen SET email = ?, telefoonnr = ?, bijzonderheden_beschikbaarheid = ?, kort_voorstellen = ? WHERE id = ?;