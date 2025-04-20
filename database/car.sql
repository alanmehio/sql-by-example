BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "car" (
	"id"	INTEGER,
	"description"	TEXT,
	"price"	REAL,
	"mileage "	REAL,
	"manufacturer_id"	INTEGER,
	"seller_id"	INTEGER,
	"sold"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("manufacturer_id") REFERENCES "manufacturer"("id"),
	FOREIGN KEY("seller_id") REFERENCES ""
);
CREATE TABLE IF NOT EXISTS "manufacturer" (
	"id"	INTEGER,
	"name"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "seller" (
	"id"	INTEGER,
	"name"	TEXT,
	"email"	TEXT,
	"address"	TEXT,
	"telephone"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
