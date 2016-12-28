/*
 Navicat MySQL Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50711
 Source Host           : localhost
 Source Database       : it_asset

 Target Server Type    : MySQL
 Target Server Version : 50711
 File Encoding         : utf-8

 Date: 12/23/2016 14:22:22 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `Authorization`
-- ----------------------------
DROP TABLE IF EXISTS `Authorization`;
CREATE TABLE `Authorization` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `module_id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `Idc`
-- ----------------------------
DROP TABLE IF EXISTS `Idc`;
CREATE TABLE `Idc` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `idc_name` varchar(24) NOT NULL,
  `rack_number` varchar(8) NOT NULL,
  `start_time` int(11) NOT NULL,
  `end_time` int(11) NOT NULL,
  `service_provider` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `Idc`
-- ----------------------------
BEGIN;
INSERT INTO `Idc` VALUES ('12', 'jg-1', '1', '1481684196', '1544756199', '2'), ('13', 'jg-2', '2', '1481626596', '1544698599', '1'), ('14', 'jg-3', '3', '1481626596', '1544698599', '1'), ('15', 'jg-4', '4', '1481655396', '1544727399', '1'), ('16', 'jg-5', '5', '1481626596', '1544698599', '1'), ('17', 'jg-6', '6', '1481626596', '1544698599', '1'), ('19', 'jg-7-1', '7', '1481790879', '1482050081', '1');
COMMIT;

-- ----------------------------
--  Table structure for `Module`
-- ----------------------------
DROP TABLE IF EXISTS `Module`;
CREATE TABLE `Module` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `module_name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `Network_config`
-- ----------------------------
DROP TABLE IF EXISTS `Network_config`;
CREATE TABLE `Network_config` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `idc_name` varchar(256) NOT NULL,
  `manage_ip` varchar(256) NOT NULL,
  `other_ip` varchar(256) NOT NULL,
  `dev_type` int(11) NOT NULL,
  `dev_ports` varchar(255) DEFAULT NULL,
  `sn` varchar(255) DEFAULT NULL,
  `an` varchar(255) DEFAULT NULL,
  `units` varchar(255) DEFAULT NULL,
  `rack_number` varchar(255) DEFAULT NULL,
  `rack_units` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idc_name` (`idc_name`),
  UNIQUE KEY `other_ip` (`other_ip`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `Network_config`
-- ----------------------------
BEGIN;
INSERT INTO `Network_config` VALUES ('1', '7', '192.168.0.255', '192.168.0.154', '1', '80', '124', '111', '111', '13', '1-1'), ('2', '1', '192.168.0.253', '192.168.0.254', '2', '901', '1', '2', '12', '12', '12');
COMMIT;

-- ----------------------------
--  Table structure for `Room`
-- ----------------------------
DROP TABLE IF EXISTS `Room`;
CREATE TABLE `Room` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `room_name` varchar(256) NOT NULL,
  `room_addr` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `Room`
-- ----------------------------
BEGIN;
INSERT INTO `Room` VALUES ('11', '北京', '上海市'), ('12', '北京', '上海市'), ('13', '北京dafaf', '上海市'), ('14', '北京', '上海市'), ('15', '北京', '上海市'), ('16', '测试中文添加', '上海市');
COMMIT;

-- ----------------------------
--  Table structure for `Server`
-- ----------------------------
DROP TABLE IF EXISTS `Server`;
CREATE TABLE `Server` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增加ID',
  `hostname` varchar(24) NOT NULL COMMENT '主机名称',
  `manage_ip` varchar(255) NOT NULL COMMENT '管理IP',
  `other_ip` varchar(256) NOT NULL COMMENT '其它IP',
  `app_name` varchar(256) NOT NULL COMMENT '应用名称',
  `system_version` varchar(255) DEFAULT NULL COMMENT '系统版本',
  `zabbix_template` smallint(10) DEFAULT NULL COMMENT '监控模版ID',
  `owner_group` smallint(10) DEFAULT NULL COMMENT '所属组id',
  `server_type` smallint(10) DEFAULT NULL COMMENT '服务器类型',
  `cpu` varchar(255) DEFAULT NULL COMMENT '服务器cpu型号',
  `mem` varchar(255) DEFAULT NULL COMMENT '服务器内存型号',
  `disk` varchar(255) DEFAULT NULL COMMENT '服务器硬盘型号',
  `sn` varchar(255) DEFAULT NULL COMMENT '服务器sn号',
  `an` varchar(255) DEFAULT NULL COMMENT '服务器an号',
  `units` varchar(255) DEFAULT NULL COMMENT '服务器单元',
  `idc_name` smallint(10) DEFAULT NULL COMMENT '服务器所在机房ID',
  `rack_number` smallint(10) DEFAULT NULL COMMENT '服务器所在机柜ID',
  `rack_units` smallint(10) DEFAULT NULL COMMENT '服务器所在机柜单元',
  `create_date` varchar(256) DEFAULT NULL COMMENT '服务器购买日期',
  `end_date` varchar(256) DEFAULT NULL COMMENT '服务器过保日期',
  `switch_name` smallint(10) DEFAULT NULL COMMENT '网络设备ID',
  `switch_port` smallint(10) DEFAULT NULL COMMENT '网络端口ID',
  `change_time` int(11) DEFAULT NULL COMMENT '服务器变更时间',
  `change_dev_info` varchar(256) DEFAULT NULL COMMENT '开发变更信息',
  `change_people` varchar(256) DEFAULT NULL COMMENT '变更人',
  `description` varchar(255) DEFAULT NULL COMMENT '描述',
  `status` tinyint(1) DEFAULT NULL COMMENT '服务器状态 0=机器通电且没有服务运行 1=服务运行 2=停机',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `Server`
-- ----------------------------
BEGIN;
INSERT INTO `Server` VALUES ('2', 'fang-vpn', '192.168.0.253', '192.168.0.254', 'app1', 'centos-v6', '1', '1', '1', '32', '64', '2TB', '1', '111', '111', '1', '1', '11', '2016-12-13 14:60:28', '2018-12-12 14:60:33', '1111', '11111', null, null, null, '1111', '1'), ('4', 'fang-vpn-1', '192.168.1.2', '192.168.1.3', 'app-vpn-server', 'ubuntu12', '1', '1', '1', '12', '32', '2TB', '1', '1', '1', '7', '15', '12', '2016-12-15 16:31:56', '2016-12-31 16:31:59', '1', '12', '1481792022', 'change change-people notes', '1111', '1111', '0');
COMMIT;

-- ----------------------------
--  Table structure for `Server_type`
-- ----------------------------
DROP TABLE IF EXISTS `Server_type`;
CREATE TABLE `Server_type` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `Service_provider`
-- ----------------------------
DROP TABLE IF EXISTS `Service_provider`;
CREATE TABLE `Service_provider` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Service_provider_name` varchar(256) NOT NULL,
  `Service_provider_addr` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Service_provider_name` (`Service_provider_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `Service_provider`
-- ----------------------------
BEGIN;
INSERT INTO `Service_provider` VALUES ('1', 'shang wan net', 'shanghai111'), ('2', 'shang ucloud', 'yangpuqu1111'), ('3', 'srv-1', 'srv-shanghai-1');
COMMIT;

-- ----------------------------
--  Table structure for `VM`
-- ----------------------------
DROP TABLE IF EXISTS `VM`;
CREATE TABLE `VM` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增加ID',
  `hostname` varchar(256) NOT NULL COMMENT '主机名称',
  `manage_ip` varchar(256) NOT NULL COMMENT '管理IP',
  `other_ip` varchar(256) NOT NULL COMMENT '其它IP',
  `app_name` varchar(256) NOT NULL COMMENT '应用名称',
  `system_version` varchar(255) DEFAULT NULL COMMENT '系统版本',
  `zabbix_template` smallint(10) DEFAULT NULL COMMENT '监控模版ID',
  `owner_group` smallint(10) DEFAULT NULL COMMENT '所属组id',
  `cpu` varchar(255) DEFAULT NULL COMMENT '服务器cpu型号',
  `mem` varchar(255) DEFAULT NULL COMMENT '服务器内存型号',
  `disk` varchar(255) DEFAULT NULL COMMENT '服务器硬盘型号',
  `hypervisor_host` varchar(255) DEFAULT NULL COMMENT '宿主机ip',
  `change_time` int(11) DEFAULT NULL COMMENT '服务器变更时间',
  `change_dev_info` varchar(256) DEFAULT NULL COMMENT '开发变更信息',
  `change_people` varchar(64) DEFAULT NULL COMMENT '变更人',
  `description` varchar(255) DEFAULT NULL COMMENT '描述',
  `status` tinyint(1) DEFAULT NULL COMMENT '服务器状态 0=机器通电且没有服务运行 1=服务运行 2=停机',
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  UNIQUE KEY `other_ip` (`other_ip`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `VM`
-- ----------------------------
BEGIN;
INSERT INTO `VM` VALUES ('1', 'vm-MongoDB-Master_server_1', '192.168.0.253', '192.168.0.254', 'app1', 'centos-v6', '1', '1', '32', '64', '2TB', '192.168.0.111', null, null, null, 'qqqqq', '0'), ('2', 'vm-cloud-1', '192.168.1.3', '192.168.1.4', 'MySQL_SALAVE', 'centos-v6', '1', '1', '13', '16', '12G', '192.168.1.1', null, 'change change-people notes', '1111', '192.168.1.3', '1');
COMMIT;

-- ----------------------------
--  Table structure for `auth_group`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `auth_group_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `auth_permission`
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `auth_permission`
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry'), ('2', 'Can change log entry', '1', 'change_logentry'), ('3', 'Can delete log entry', '1', 'delete_logentry'), ('4', 'Can add permission', '2', 'add_permission'), ('5', 'Can change permission', '2', 'change_permission'), ('6', 'Can delete permission', '2', 'delete_permission'), ('7', 'Can add group', '3', 'add_group'), ('8', 'Can change group', '3', 'change_group'), ('9', 'Can delete group', '3', 'delete_group'), ('10', 'Can add user', '4', 'add_user'), ('11', 'Can change user', '4', 'change_user'), ('12', 'Can delete user', '4', 'delete_user'), ('13', 'Can add content type', '5', 'add_contenttype'), ('14', 'Can change content type', '5', 'change_contenttype'), ('15', 'Can delete content type', '5', 'delete_contenttype'), ('16', 'Can add session', '6', 'add_session'), ('17', 'Can change session', '6', 'change_session'), ('18', 'Can delete session', '6', 'delete_session'), ('19', 'Can add employee', '7', 'add_employee'), ('20', 'Can change employee', '7', 'change_employee'), ('21', 'Can delete employee', '7', 'delete_employee');
COMMIT;

-- ----------------------------
--  Table structure for `auth_user`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `auth_user`
-- ----------------------------
BEGIN;
INSERT INTO `auth_user` VALUES ('1', 'pbkdf2_sha256$12000$ayEJzSdqGpfY$da7Cnk8ixleXIqlujC/4GcT3S4w1QJt/zQDZy6C88bY=', '2016-12-11 20:30:05', '1', 'fanghouguo', '', '', 'fanghouguo@sina.com', '1', '1', '2016-12-11 20:30:05'), ('4', 'pbkdf2_sha256$12000$mQ4zuhwlLWTf$t8GAfNa6Tqrh+KnyHyDMGXBAvMIyGb9kI1X36zSxAaU=', '2016-12-23 06:11:29', '1', 'demo', '', '', 'demo@sina.com', '1', '1', '2016-12-23 06:03:21');
COMMIT;

-- ----------------------------
--  Table structure for `auth_user_groups`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `auth_user_user_permissions`
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `django_admin_log`
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `django_content_type`
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES ('1', 'log entry', 'admin', 'logentry'), ('2', 'permission', 'auth', 'permission'), ('3', 'group', 'auth', 'group'), ('4', 'user', 'auth', 'user'), ('5', 'content type', 'contenttypes', 'contenttype'), ('6', 'session', 'sessions', 'session'), ('7', 'employee', 'app', 'employee');
COMMIT;

-- ----------------------------
--  Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `django_migrations`
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2016-12-11 20:29:25'), ('2', 'auth', '0001_initial', '2016-12-11 20:29:26'), ('3', 'admin', '0001_initial', '2016-12-11 20:29:26'), ('4', 'sessions', '0001_initial', '2016-12-11 20:29:26');
COMMIT;

-- ----------------------------
--  Table structure for `django_session`
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `django_session`
-- ----------------------------
BEGIN;
INSERT INTO `django_session` VALUES ('v9qpsbsv4m2jsdn02nlzt6rvc7z6j9ye', 'NDc1Yzk3ZmZjYmEzN2ZjYzI3MjU0YTJiMWY0Yzg4YzhhYTJhZTI4ZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjllNTA2NzZhNDY4ZGExNGQ5YjQ0NGIwYmUzMmQxNTFiMWFlNzU5ZWIiLCJfYXV0aF91c2VyX2lkIjo0LCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2017-01-06 06:11:29');
COMMIT;

-- ----------------------------
--  Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(32) NOT NULL,
  `user_passwd` varchar(512) DEFAULT NULL,
  `client_ip` varchar(64) NOT NULL,
  `auth_group` varchar(255) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `user_name` (`user_name`),
  UNIQUE KEY `client_ip` (`client_ip`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `users`
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES ('1', 'fanghouguo', 'pbkdf2_sha256$12000$L7Cu75dt9qAh$JzADhK5B5OULtIYwG3HHLNzepckO1LteExD/Kzv4GpE=', '127.0.0.1', '1');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
