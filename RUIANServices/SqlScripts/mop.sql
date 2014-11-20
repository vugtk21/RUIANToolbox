drop table if exists ui_mop;
CREATE TABLE ui_mop
(
  kod character varying,
  nazev character varying,
  obec_kod integer
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ui_mop
  OWNER TO postgres;

INSERT INTO ui_mop VALUES ('19','Praha 1',554782);
INSERT INTO ui_mop VALUES ('27','Praha 2',554782);
INSERT INTO ui_mop VALUES ('35','Praha 3',554782);
INSERT INTO ui_mop VALUES ('43','Praha 4',554782);
INSERT INTO ui_mop VALUES ('51','Praha 5',554782);
INSERT INTO ui_mop VALUES ('60','Praha 6',554782);
INSERT INTO ui_mop VALUES ('78','Praha 7',554782);
INSERT INTO ui_mop VALUES ('86','Praha 8',554782);
INSERT INTO ui_mop VALUES ('94','Praha 9',554782);
INSERT INTO ui_mop VALUES ('108','Praha 10',554782);
