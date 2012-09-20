/*
 Navicat Premium Data Transfer

 Source Server         : SBC
 Source Server Type    : SQLite
 Source Server Version : 3007010
 Source Database       : main

 Target Server Type    : SQLite
 Target Server Version : 3007010
 File Encoding         : utf-8

 Date: 09/19/2012 13:27:42 PM
*/

PRAGMA foreign_keys = false;

-- ----------------------------
--  Table structure for "Web_alerta"
-- ----------------------------
DROP TABLE IF EXISTS "Web_alerta";
CREATE TABLE "Web_alerta" (
    "id" integer NOT NULL PRIMARY KEY,
    "operadorid_id" integer NOT NULL REFERENCES "Web_operador" ("id"),
    "tipo" varchar(30) NOT NULL,
    "nivel" varchar(30) NOT NULL,
    "mensaje" text NOT NULL,
    "enviado" date NOT NULL
);

-- ----------------------------
--  Table structure for "Web_cargas"
-- ----------------------------
DROP TABLE IF EXISTS "Web_cargas";
CREATE TABLE "Web_cargas" (
    "id" integer NOT NULL PRIMARY KEY,
    "servidorid_id" integer NOT NULL REFERENCES "Web_servidor" ("id"),
    "time_unix" varchar(30) NOT NULL,
    "cpu_total" real NOT NULL,
    "cpu_cores" varchar(30) NOT NULL,
    "mem_total" integer NOT NULL,
    "mem_used" integer NOT NULL,
    "mem_free" integer NOT NULL,
    "mem_percent" varchar(30) NOT NULL,
    "io_read_count" integer NOT NULL,
    "io_write_count" integer NOT NULL,
    "io_read_bytes" integer NOT NULL,
    "io_write_bytes" integer NOT NULL,
    "io_read_time" integer NOT NULL,
    "io_write_time" integer NOT NULL,
    "net_bytes_sent" integer NOT NULL,
    "net_bytes_recv" integer NOT NULL,
    "net_packets_sent" integer NOT NULL,
    "net_packets_recv" integer NOT NULL,
    "hdd_device" varchar(30) NOT NULL,
    "hdd_total" integer NOT NULL,
    "hdd_used" integer NOT NULL,
    "hdd_free" integer NOT NULL,
    "hdd_percent" varchar(30) NOT NULL
);

-- ----------------------------
--  Table structure for "Web_configuracion"
-- ----------------------------
DROP TABLE IF EXISTS "Web_configuracion";
CREATE TABLE "Web_configuracion" (
    "id" integer NOT NULL PRIMARY KEY,
    "agente" varchar(30) NOT NULL,
    "clave" varchar(30) NOT NULL,
    "valor" varchar(30) NOT NULL,
    "modificado" varchar(30) NOT NULL,
    "defvalor" varchar(30) NOT NULL,
    "prevalor" varchar(30) NOT NULL
);

-- ----------------------------
--  Table structure for "Web_operador"
-- ----------------------------
DROP TABLE IF EXISTS "Web_operador";
CREATE TABLE "Web_operador" (
    "id" integer NOT NULL PRIMARY KEY,
    "nombre" varchar(30) NOT NULL,
    "clave" varchar(10) NOT NULL,
    "correo" varchar(20) NOT NULL,
    "jid" varchar(20) NOT NULL
);

-- ----------------------------
--  Table structure for "Web_servidor"
-- ----------------------------
DROP TABLE IF EXISTS "Web_servidor";
CREATE TABLE "Web_servidor" (
    "id" integer NOT NULL PRIMARY KEY,
    "fqdn" varchar(30) NOT NULL,
    "puerto" integer NOT NULL,
    "activo" bool NOT NULL,
    "modificado" varchar(30) NOT NULL,
    "intento" integer NOT NULL
);

-- ----------------------------
--  Table structure for "auth_group"
-- ----------------------------
DROP TABLE IF EXISTS "auth_group";
CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
);

-- ----------------------------
--  Table structure for "auth_group_permissions"
-- ----------------------------
DROP TABLE IF EXISTS "auth_group_permissions";
CREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
);

-- ----------------------------
--  Table structure for "auth_message"
-- ----------------------------
DROP TABLE IF EXISTS "auth_message";
CREATE TABLE "auth_message" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "message" text NOT NULL
);

-- ----------------------------
--  Table structure for "auth_permission"
-- ----------------------------
DROP TABLE IF EXISTS "auth_permission";
CREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);

-- ----------------------------
--  Table structure for "auth_user"
-- ----------------------------
DROP TABLE IF EXISTS "auth_user";
CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "is_superuser" bool NOT NULL,
    "last_login" datetime NOT NULL,
    "date_joined" datetime NOT NULL
);

-- ----------------------------
--  Table structure for "auth_user_groups"
-- ----------------------------
DROP TABLE IF EXISTS "auth_user_groups";
CREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
);

-- ----------------------------
--  Table structure for "auth_user_user_permissions"
-- ----------------------------
DROP TABLE IF EXISTS "auth_user_user_permissions";
CREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
);

-- ----------------------------
--  Table structure for "django_admin_log"
-- ----------------------------
DROP TABLE IF EXISTS "django_admin_log";
CREATE TABLE "django_admin_log" (
    "id" integer NOT NULL PRIMARY KEY,
    "action_time" datetime NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "content_type_id" integer REFERENCES "django_content_type" ("id"),
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint unsigned NOT NULL,
    "change_message" text NOT NULL
);

-- ----------------------------
--  Table structure for "django_content_type"
-- ----------------------------
DROP TABLE IF EXISTS "django_content_type";
CREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
);

-- ----------------------------
--  Table structure for "django_session"
-- ----------------------------
DROP TABLE IF EXISTS "django_session";
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" datetime NOT NULL
);

-- ----------------------------
--  Table structure for "django_site"
-- ----------------------------
DROP TABLE IF EXISTS "django_site";
CREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
);

-- ----------------------------
--  Indexes structure for table "Web_alerta"
-- ----------------------------
CREATE INDEX "Web_alerta_f252d6d1" ON "Web_alerta" ("operadorid_id");

-- ----------------------------
--  Indexes structure for table "Web_cargas"
-- ----------------------------
CREATE INDEX "Web_cargas_40aca237" ON "Web_cargas" ("servidorid_id");

-- ----------------------------
--  Indexes structure for table "auth_group_permissions"
-- ----------------------------
CREATE INDEX "auth_group_permissions_bda51c3c" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_1e014c8f" ON "auth_group_permissions" ("permission_id");

-- ----------------------------
--  Indexes structure for table "auth_message"
-- ----------------------------
CREATE INDEX "auth_message_fbfc09f1" ON "auth_message" ("user_id");

-- ----------------------------
--  Indexes structure for table "auth_permission"
-- ----------------------------
CREATE INDEX "auth_permission_e4470c6e" ON "auth_permission" ("content_type_id");

-- ----------------------------
--  Indexes structure for table "auth_user_groups"
-- ----------------------------
CREATE INDEX "auth_user_groups_fbfc09f1" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_bda51c3c" ON "auth_user_groups" ("group_id");

-- ----------------------------
--  Indexes structure for table "auth_user_user_permissions"
-- ----------------------------
CREATE INDEX "auth_user_user_permissions_fbfc09f1" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_1e014c8f" ON "auth_user_user_permissions" ("permission_id");

-- ----------------------------
--  Indexes structure for table "django_admin_log"
-- ----------------------------
CREATE INDEX "django_admin_log_fbfc09f1" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_e4470c6e" ON "django_admin_log" ("content_type_id");

-- ----------------------------
--  Indexes structure for table "django_session"
-- ----------------------------
CREATE INDEX "django_session_c25c2c28" ON "django_session" ("expire_date");

PRAGMA foreign_keys = true;
