/* DROP TABLE IF EXISTS & CREATING THEM*/
USE PY_ELT_Acquisition_Db;

DROP TABLE IF EXISTS CreditScore;

CREATE TABLE CreditScore(
	Age					VARCHAR(255) NOT NULL,
	Gender				VARCHAR(255) NOT NULL,
	Income				VARCHAR(255) NOT NULL,
	Education			VARCHAR(255) NOT NULL,
	MaritalStatus		VARCHAR(255) NOT NULL,
	NumberOfChildren	VARCHAR(255) NOT NULL,
	HomeOwnership		VARCHAR(255) NOT NULL,
	CreditScore			VARCHAR(255) NOT NULL
)
CREATE INDEX IndexCreditScore ON CreditScore (CreditScore)
;