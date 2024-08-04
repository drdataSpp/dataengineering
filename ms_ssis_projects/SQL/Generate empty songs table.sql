USE [DEV_SSIS_DB]
GO

DROP TABLE IF EXISTS MillionSellers
GO

CREATE TABLE MillionSellers(
	Artist varchar(255),
	Sales decimal(10,2),
	Title varchar(255),
	SongYear int
)

GO