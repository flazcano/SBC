/*
 Navicat Premium Data Transfer

 Source Server         : SBC
 Source Server Type    : SQLite
 Source Server Version : 3007006
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3007006
 File Encoding         : utf-8

 Date: 11/15/2011 23:18:46 PM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for "alerta"
-- ----------------------------
DROP TABLE IF EXISTS "alerta";
CREATE TABLE "alerta" (
	 "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	 "operadorid" INTEGER NOT NULL,
	 "tipo" TEXT NOT NULL,
	 "nivel" TEXT NOT NULL,
	 "mensaje" TEXT NOT NULL,
	CONSTRAINT "fk_id_op" FOREIGN KEY ("operadorid") REFERENCES "operador" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
--  Table structure for "carga"
-- ----------------------------
DROP TABLE IF EXISTS "carga";
CREATE TABLE "carga" (
	 "id" INTEGER NOT NULL,
	 "servidorid" INTEGER NOT NULL,
	 "time_unix" TEXT NOT NULL,
	 "cpu_total" FLOAT NOT NULL,
	 "cpu_cores" TEXT NOT NULL,
	 "mem_total" INTEGER NOT NULL,
	 "mem_used" INTEGER NOT NULL,
	 "mem_free" INTEGER NOT NULL,
	 "mem_percent" FLOAT NOT NULL,
	 "io_read_count" INTEGER NOT NULL,
	 "io_write_count" INTEGER NOT NULL,
	 "io_read_bytes" INTEGER NOT NULL,
	 "io_write_bytes" INTEGER NOT NULL,
	 "io_read_time" INTEGER NOT NULL,
	 "io_write_time" INTEGER NOT NULL,
	 "net_bytes_sent" INTEGER NOT NULL,
	 "net_bytes_recv" INTEGER NOT NULL,
	 "net_packets_sent" INTEGER NOT NULL,
	 "net_packets_recv" INTEGER NOT NULL,
	 "hdd_device" TEXT NOT NULL,
	 "hdd_total" INTEGER NOT NULL,
	 "hdd_used" INTEGER NOT NULL,
	 "hdd_free" INTEGER NOT NULL,
	 "hdd_percent" FLOAT NOT NULL,
	PRIMARY KEY("id"),
	CONSTRAINT "fk_id_srv" FOREIGN KEY ("servidorid") REFERENCES "servidor" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
--  Table structure for "configuracion"
-- ----------------------------
DROP TABLE IF EXISTS "configuracion";
CREATE TABLE "configuracion" (
	 "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	 "agente" TEXT NOT NULL,
	 "clave" TEXT NOT NULL,
	 "valor" TEXT NOT NULL,
	 "modificado" TEXT NOT NULL,
	 "defvalor" TEXT NOT NULL,
	 "prevalor" TEXT,
	UNIQUE (clave ASC)
);

-- ----------------------------
--  Table structure for "operador"
-- ----------------------------
DROP TABLE IF EXISTS "operador";
CREATE TABLE "operador" (
	 "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	 "nombre" TEXT NOT NULL,
	 "clave" TEXT NOT NULL,
	 "correo" TEXT NOT NULL,
	 "jid" TEXT NOT NULL
);

-- ----------------------------
--  Table structure for "servidor"
-- ----------------------------
DROP TABLE IF EXISTS "servidor";
CREATE TABLE "servidor" (
	 "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	 "fqdn" TEXT NOT NULL,
	 "puerto" INTEGER NOT NULL DEFAULT 54321,
	 "activo" BOOLEAN NOT NULL DEFAULT TRUE,
	 "modificado" TEXT NOT NULL,
	 "intento" INTEGER NOT NULL DEFAULT 0,
	UNIQUE (fqdn ASC)
);

-- ----------------------------
--  Records of "servidor"
-- ----------------------------
BEGIN;
INSERT INTO "servidor" VALUES (1, '192.168.0.2', 54321, X'54525545', 1320634947.06983, 0);
COMMIT;

PRAGMA foreign_keys = true;
