/* DROP VIEW IF EXISTS & CREATING THEM*/
USE PY_ELT_Acquisition_Db;

DROP VIEW IF EXISTS CreditScore_V;

CREATE VIEW CreditScore_V AS
SELECT 
	T.Age			   AS Age,	
	T.Gender		   AS Gender,	
	T.Income		   AS Income,					
	T.Education		   AS Education,		
	T.MaritalStatus	   AS MaritalStatus,			
	T.NumberOfChildren AS NumberOfChildren,
	T.HomeOwnership	   AS HomeOwnership,	
	T.CreditScore	   AS CreditScore	
FROM CreditScore AS T
;