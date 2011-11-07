/*
 Navicat Premium Data Transfer

 Source Server         : SBC
 Source Server Type    : SQLite
 Source Server Version : 3007006
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3007006
 File Encoding         : utf-8

 Date: 11/07/2011 00:01:15 AM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for "cargas"
-- ----------------------------
DROP TABLE IF EXISTS "cargas";
CREATE TABLE "cargas" (
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
	CONSTRAINT "fk_id_srv" FOREIGN KEY ("servidorid") REFERENCES "servidor" ("id") ON DELETE CASCADE
);

-- ----------------------------
--  Table structure for "configuracion"
-- ----------------------------
DROP TABLE IF EXISTS "configuracion";
CREATE TABLE "configuracion" (id INTEGER NOT NULL PRIMARY KEY, clave TEXT UNIQUE NOT NULL, valor TEXT NOT NULL, modificado TEXT NOT NULL, defvalor TEXT, prevalor TEXT);

-- ----------------------------
--  Table structure for "servidor"
-- ----------------------------
DROP TABLE IF EXISTS "servidor";
CREATE TABLE "servidor" (
	 "id" INTEGER NOT NULL,
	 "fqdn" TEXT NOT NULL,
	 "puerto" INTEGER NOT NULL,
	 "activo" BOOLEAN NOT NULL DEFAULT TRUE,
	 "modificado" TEXT NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE (fqdn ASC)
);

PRAGMA foreign_keys = true;
