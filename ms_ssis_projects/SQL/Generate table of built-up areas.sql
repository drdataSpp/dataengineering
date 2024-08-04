USE DEV_SSIS_DB;

DROP TABLE IF EXISTS UKBuiltUpAreas
GO

CREATE TABLE UKBuiltUpAreas(
	Rank int NULL,
	AreaName varchar(255) NULL,
	Population bigint NULL
)

GO