drop table if exists typ_st_objektu;
CREATE TABLE typ_st_objektu
(
  kod integer NOT NULL,
  nazev character varying NOT NULL,
  popis character varying,
  zkratka character varying,
  CONSTRAINT typ_st_objektu_pkey PRIMARY KEY (kod)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE typ_st_objektu
  OWNER TO postgres;

INSERT INTO typ_st_objektu VALUES (1,'Budova s číslem popisným','Budova s číslem popisným','č.p.');
INSERT INTO typ_st_objektu VALUES (2,'Budova s číslem evidenčním','Budova s číslem evidenčním','č.ev.');
INSERT INTO typ_st_objektu VALUES (3,'Budova bez č.p. a č.ev.','Budova bez čísla popisného a bez čísla evidenčního','');
