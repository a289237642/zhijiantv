/*
 Navicat Premium Data Transfer

 Source Server         : online
 Source Server Type    : MySQL
 Source Server Version : 50616
 Source Host           : rm-uf6gw23j409s5ui7qmoo.mysql.rds.aliyuncs.com:3306
 Source Schema         : zhijiantv

 Target Server Type    : MySQL
 Target Server Version : 50616
 File Encoding         : 65001

 Date: 10/06/2019 13:23:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('921f709b1835');

-- ----------------------------
-- Table structure for tv_user_info
-- ----------------------------
DROP TABLE IF EXISTS `tv_user_info`;
CREATE TABLE `tv_user_info`  (
  `create_time` datetime(0) DEFAULT NULL,
  `update_time` datetime(0) DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `pass_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `siuper` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  INDEX `ix_tv_user_info_admin_id`(`admin_id`) USING BTREE,
  INDEX `ix_tv_user_info_pass_word`(`pass_word`(191)) USING BTREE,
  INDEX `ix_tv_user_info_status`(`status`(191)) USING BTREE,
  INDEX `ix_tv_user_info_user_name`(`user_name`(191)) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tv_user_info
-- ----------------------------
INSERT INTO `tv_user_info` VALUES ('2019-05-21 10:22:03', '2019-05-21 10:22:06', NULL, 1, 'admin', '4297f44b13955235245b2497399d7a93', '1', NULL);

-- ----------------------------
-- Table structure for tv_video_info
-- ----------------------------
DROP TABLE IF EXISTS `tv_video_info`;
CREATE TABLE `tv_video_info`  (
  `create_time` datetime(0) DEFAULT NULL,
  `update_time` datetime(0) DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vtype` int(11) DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `summary` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `pic_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `play_nums` int(11) DEFAULT NULL,
  `play_times` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `is_show` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  INDEX `vtype`(`vtype`) USING BTREE,
  INDEX `ix_tv_video_info_admin_id`(`admin_id`) USING BTREE,
  INDEX `ix_tv_video_info_is_show`(`is_show`) USING BTREE,
  INDEX `ix_tv_video_info_status`(`status`) USING BTREE,
  INDEX `ix_tv_video_info_title`(`title`(191)) USING BTREE,
  CONSTRAINT `tv_video_info_ibfk_1` FOREIGN KEY (`vtype`) REFERENCES `tv_video_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 150 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tv_video_info
-- ----------------------------
INSERT INTO `tv_video_info` VALUES ('2019-06-03 14:29:41', '2019-06-10 11:44:51', NULL, 31, 44, '半年没给员工开工资，靠什么撑到现在', '', 'https://oss.max-tv.net.cn/1559543266r0i9f5luvxW,W,Q,X1559543236235', 'https://oss.max-tv.net.cn/1559543344r6wfv0isgt半年没给员工开工资，靠什么撑到现在.jpg', 53, '03:25', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 14:36:25', '2019-06-10 11:43:57', NULL, 32, 44, '从办公家具转型做装修，他看中的市场前景是什么？', '', 'https://oss.max-tv.net.cn/1559543607k5s7r7vxdrO,J,R,F1559543600983', 'https://oss.max-tv.net.cn/15595437554k2big7tp5从办公家具转型做装修，他看中的市场前景是什么？.jpg', 32, '03:07', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 14:39:31', '2019-06-08 01:35:41', NULL, 33, 44, '打造IP就像打高尔夫球', '', 'https://oss.max-tv.net.cn/1559543825xw7a0ox2spB,P,S,W1559543823790', 'https://oss.max-tv.net.cn/1559543947crgrmhi9fd打造IP就像打高尔夫球.jpg', 12, '02:53', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:13:03', '2019-06-08 09:41:50', NULL, 34, 44, '低频项目如何找到持续盈利的商业模式？', '', 'https://oss.max-tv.net.cn/1559544003wlvzv7fg7cZ,O,R,C1559544001779', 'https://oss.max-tv.net.cn/1559544076is60v710ih低频项目如何找到持续盈利的商业模式？-.jpg', 6, '03:02', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:15:56', '2019-06-10 11:59:51', NULL, 35, 44, '对标MIT团队做光子AI芯片，迟到4个月为何获得英诺青睐？', '', 'https://oss.max-tv.net.cn/1559545997m3a7hj5gp1U,Y,M,P1559545993439', 'https://oss.max-tv.net.cn/1559546121fwkco0m266对标MIT团队做光子AI芯片，迟到4个月为何获得英诺青睐？.jpg', 15, '02:40', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:36:36', '2019-06-08 08:34:04', NULL, 36, 44, '赶超“雷电”销量最好的SD游戏  7年积累还差最后一步？', '', 'https://oss.max-tv.net.cn/15595472541tju12qtdlD,X,D,M1559547252449', 'https://oss.max-tv.net.cn/1559547373o09gd2z8ke赶超“雷电”销量最好的SD游戏  7年积累还差最后一步？.jpg', 11, '02:45', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:39:46', '2019-06-08 20:33:07', NULL, 37, 44, '高速公路要普及人脸识别', '', 'https://oss.max-tv.net.cn/15595474134iyxv3ffv7U,I,G,D1559547411940', 'https://oss.max-tv.net.cn/1559547474dw8rkrr9ml高速公路要普及人脸识别.jpg', 8, '02:11', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:42:57', '2019-06-08 08:30:25', NULL, 38, 44, '巨头早已布局电子证件 迟到的“收纳通”新意何在？', '', 'https://oss.max-tv.net.cn/1559547682sdcx2tqun8N,G,K,W1559547680618', 'https://oss.max-tv.net.cn/1559547754be1wxk6h6m巨头早已布局电子证件 迟到的“收纳通”新意何在？.jpg', 9, '02:47', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:45:13', '2019-06-10 12:00:09', NULL, 39, 44, '开个航校专招青少年？', '', 'https://oss.max-tv.net.cn/155954780254ctx3cul3Y,B,P,L1559547801020', 'https://oss.max-tv.net.cn/1559547891c4dojmiih6开个航校专招青少年？.jpg', 7, '02:46', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:49:20', '2019-06-08 01:19:00', NULL, 40, 44, '靠蚂蚁浏览器自给自足5年 转战人脸识别优势何在？', '', 'https://oss.max-tv.net.cn/1559547994us6jtwudbsB,H,R,H1559547993337', 'https://oss.max-tv.net.cn/1559548108l7r7chvse3靠蚂蚁浏览器自给自足5年 转战人脸识别优势何在？-.jpg', 6, '02:49', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:51:39', '2019-06-08 17:44:00', NULL, 41, 44, '靠同城配送起家的生鲜新手 PK美菜靠什么？', '', 'https://oss.max-tv.net.cn/1559548177ankzvg97t4S,Z,N,T1559548174172', 'https://oss.max-tv.net.cn/15595482715kmusperrp靠同城配送起家的生鲜新手 PK美菜靠什么？.jpg', 6, '02:49', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:55:18', '2019-06-08 05:00:42', NULL, 42, 44, '联合创业产业新打法，传统产业园区未来的发展模式', '', 'https://oss.max-tv.net.cn/1559548306yxa2ca2p7aD,K,L,W1559548305627', 'https://oss.max-tv.net.cn/1559548494vkt5w7m5bo联合创业产业新打法，传统产业园区未来的发展模式.jpg', 6, '03:05', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 15:58:49', '2019-06-08 11:25:28', NULL, 44, 44, '新零售时代，这样卖酒是否可行？', '', 'https://oss.max-tv.net.cn/15595485279ms3fkxi8yN,Y,Q,F1559548526243', 'https://oss.max-tv.net.cn/15595487065tbd8k8s38美酒佳肴新零售 吴文波.jpg', 8, '02:55', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 16:01:38', '2019-06-10 12:00:02', NULL, 45, 44, '商场自拍试衣镜，能成功导流吗？', '', 'https://oss.max-tv.net.cn/155954876798l02wzczkC,P,R,K1559548765846', 'https://oss.max-tv.net.cn/1559548868me86qoymud商场自拍试衣镜，能成功导流吗？.jpg', 5, '02:24', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 17:12:31', '2019-06-10 11:53:24', NULL, 47, 44, '体育大潮下 小众民族特色体育项目如何走出特色之路', '', 'https://oss.max-tv.net.cn/15595531318ksd0b6cl6P,M,E,J1559552987092', 'https://oss.max-tv.net.cn/1559553128i3t9q3j9qw体育大潮下 小众民族特色体育项目如何走出特色之路-.jpg', 8, '02:56', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 17:14:38', '2019-06-08 02:58:28', NULL, 48, 44, '用漫画和电影放大IP效应，可否与巨头抗衡？', '', 'https://oss.max-tv.net.cn/1559553174wqahz0mc6uF,N,E,S1559553172029', 'https://oss.max-tv.net.cn/1559553253576t1tiov4用漫画和电影放大IP效应，可否与巨头抗衡？-.jpg', 4, '02:56', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 17:16:42', '2019-06-08 09:01:59', NULL, 49, 44, '掌上菜市场用户7百一个月就能营收平衡？', '', 'https://oss.max-tv.net.cn/1559553289vg05dzy63xZ,T,M,P1559553287168', 'https://oss.max-tv.net.cn/15595533707l6wyf7vsg掌上菜市场用户7百一个月就能营收平衡？.jpg', 6, '02:13', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 17:18:48', '2019-06-08 09:44:52', NULL, 50, 44, '这家机器人公司有什么不同？投资人点评：接地气！', '', 'https://oss.max-tv.net.cn/1559553419ph1o0nt73zI,B,Q,J1559553417858', 'https://oss.max-tv.net.cn/1559553497pnosown8ck这家机器人公司有什么不同？投资人点评：接地气！.jpg', 8, '02:58', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-03 17:20:36', '2019-06-08 01:37:02', NULL, 51, 44, '抓紧！小程序模式创新抢占红利 时间窗口只有半年', '', 'https://oss.max-tv.net.cn/1559553538aafjjvrx1pR,I,K,Z1559553535646', 'https://oss.max-tv.net.cn/1559553610kd1to0chho抓紧！小程序模式创新抢占红利 时间窗口只有半年.jpg', 5, '02:52', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 10:01:04', '2019-06-08 00:35:06', NULL, 59, 44, '初创项目有这么多CXO', '', 'https://oss.max-tv.net.cn/1559613641qy6n1b59wwC,X,R,T1559613636063', 'https://oss.max-tv.net.cn/1559613659p8nopyk2th初创项目有这么多CXO.jpg', 3, '02:30', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 10:03:15', '2019-06-08 00:34:54', NULL, 60, 44, '丢掉铁饭碗 辛苦创业', '', 'https://oss.max-tv.net.cn/1559613745iawvkevj6dH,T,B,U1559613736013', 'https://oss.max-tv.net.cn/1559613758hk231vav4s丢掉铁饭碗 辛苦创业.jpg', 1, '02:05', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 10:06:27', '2019-06-04 10:06:27', NULL, 61, 44, '连续创业者这次是否能拿到投资', '', 'https://oss.max-tv.net.cn/1559613810taqslw8t2oS,J,F,L1559613805267', 'https://oss.max-tv.net.cn/1559613821f7l3g51w3r连续创业者这次是否能拿到投资.jpg', 0, '02:04', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 10:08:49', '2019-06-08 00:35:11', NULL, 62, 44, '移动母婴室解决社会刚需，得到投资人认可', '', 'https://oss.max-tv.net.cn/1559613997wc22gwe32cB,V,U,T1559613994358', 'https://oss.max-tv.net.cn/1559614022aol519jqf2mamain移动母婴室.png', 1, '05:59', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 13:12:01', '2019-06-04 13:12:01', NULL, 63, 44, '“滴滴打律师”美女创业能否被顶级机构看中', '', 'https://oss.max-tv.net.cn/155962504960w5d2pz91Z,I,H,N1559624924174', 'https://oss.max-tv.net.cn/155962494151nicbevqx法驳士.jpg', 0, '04:38', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 13:13:45', '2019-06-08 00:34:57', NULL, 64, 44, '一份精美的BP投资人怎么看', '', 'https://oss.max-tv.net.cn/1559625149wfbaij8k82Z,B,W,P1559625129027', 'https://oss.max-tv.net.cn/1559625157l4txk70i3g智能珠宝.jpg', 1, '07:17', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 13:56:14', '2019-06-05 14:23:59', NULL, 65, 58, '5G的战略意义大于实际意义 不适合早期投资', '', 'https://oss.max-tv.net.cn/1559627576ynnpni0obuE,S,Q,K1559627377787', 'https://oss.max-tv.net.cn/1559627757qjad77q8uc冯一名采访.jpg', 4, '03:37', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 13:59:26', '2019-06-05 14:20:01', NULL, 66, 58, '投资阶段不同则风控侧重点不同！现在知道还不晚', '', 'https://oss.max-tv.net.cn/1559627882dv2lvrfpx7J,F,V,D1559627792348', 'https://oss.max-tv.net.cn/15596278818k1mtbl7ww王培采访.jpg', 2, '03:25', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 14:06:19', '2019-06-05 15:54:36', NULL, 67, 58, '创投税的前世今生', '', 'https://oss.max-tv.net.cn/1559628305tmu1ni149qG,H,P,X1559627983546', 'https://oss.max-tv.net.cn/1559628315a1bz38yo7u王培课上.jpg', 1, '03:28', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 14:09:03', '2019-06-05 15:54:34', NULL, 68, 58, '后C端时代 下沉人群将缔造第二大主流消费群', '', 'https://oss.max-tv.net.cn/1559628465ovj17fwclrN,B,K,C1559628458350', 'https://oss.max-tv.net.cn/15596284794hcptblsqc徐晨采访.jpg', 4, '04:45', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 14:11:10', '2019-06-05 14:12:17', NULL, 69, 58, '徐晨：每个风险投资基金都有各自对其所投项目的预期回报要求', '', 'https://oss.max-tv.net.cn/1559628569vhoyfu3jr3P,M,S,K1559628566556', 'https://oss.max-tv.net.cn/15596285787wmzjpvt7e徐晨课上.jpg', 3, '02:37', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 14:12:42', '2019-06-04 14:12:42', NULL, 70, 58, '乘东风还是找漏洞？看股神如何利用哲学与市场赚钱！', '', 'https://oss.max-tv.net.cn/1559628682l9ej1sls80D,H,G,Q1559628678979', 'https://oss.max-tv.net.cn/15596286925ekku0howu苑举正采访.jpg', 0, '03:26', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 14:15:07', '2019-06-04 14:15:07', NULL, 71, 58, '跟股神学投资，结果相约天台！背后这几个重点值得深思！', '', 'https://oss.max-tv.net.cn/15596288570qy1cw2bwyQ,O,K,B1559628841501', 'https://oss.max-tv.net.cn/15596288641lako90rwd苑举正课上_1.jpg', 0, '02:35', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 16:32:27', '2019-06-05 19:12:57', NULL, 72, 59, 'O2O上门推拿幸存者', '', 'https://oss.max-tv.net.cn/1559637051uol5qzhsf6T,P,F,Y1559637046445', 'https://oss.max-tv.net.cn/1559637064ea1qssmtcz复盘第一期正片0228_1.jpg', 4, '11:10', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 16:44:05', '2019-06-04 16:44:05', NULL, 73, 59, '如果当时跟腾讯死磕到底，就不会有张小龙和微信了', '', 'https://oss.max-tv.net.cn/15596373593tqr6t2gkkD,W,B,O1559637163451', 'https://oss.max-tv.net.cn/155963737035ijb863gi复盘第二集最终版.jpg', 0, '07:29', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 17:06:55', '2019-06-04 17:06:55', NULL, 74, 59, '90后“辍学创业”：我被创业热浪催熟！', '', 'https://oss.max-tv.net.cn/1559638587k9hcswid0xQ,K,E,L1559638584733', 'https://oss.max-tv.net.cn/1559638927sajzfnayv6复盘第三期成片.jpg', 0, '10:53', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 17:12:37', '2019-06-04 17:12:37', NULL, 75, 59, '流浪汉初创业身家飙升两千万', '', 'https://oss.max-tv.net.cn/1559639380nkmbkhuxy5P,B,L,B1559639352885', 'https://oss.max-tv.net.cn/1559639419agwpbo827i复盘 第四期.jpg', 0, '07:25', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-04 17:26:53', '2019-06-04 17:26:53', NULL, 76, 59, '任何的自我膨胀都是没落的开始，', '', 'https://oss.max-tv.net.cn/1559639613942przxvnjG,M,W,X1559639610222', 'https://oss.max-tv.net.cn/1559640322humi1yddeh第五期 任牧最终版.jpg', 0, '08:11', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:12:39', '2019-06-05 14:56:51', NULL, 94, 61, '于光东：找我融资的拼多多上市了，可那时我没钱（上）', '', 'https://oss.max-tv.net.cn/15597006470t0ou8o4lkZ,X,W,I1559700348112', 'https://oss.max-tv.net.cn/155970067363ac9wjbot一拍即盒第一期01_1.jpg', 4, '09:57', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:30:08', '2019-06-05 10:31:05', NULL, 101, 61, '于光东：找我融资的拼多多上市了，可那时我没钱（中）', '', 'https://oss.max-tv.net.cn/1559701775yswirg5alnI,L,F,U1559701770425', 'https://oss.max-tv.net.cn/1559701780ohs3w93vc4一拍即盒第一期02_1.jpg', 3, '05:53', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:32:34', '2019-06-05 14:19:47', NULL, 102, 61, '于光东：找我融资的拼多多上市了，可那时我没钱（下）', '', 'https://oss.max-tv.net.cn/15597019208w82fze0oqX,M,I,K1559701910499', 'https://oss.max-tv.net.cn/1559701917ubezg8hkpt一拍即盒第一期03_1.jpg', 1, '09:17', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:33:52', '2019-06-05 10:33:52', NULL, 103, 61, '苹果是恶俗文化的带领者（上）', '', 'https://oss.max-tv.net.cn/1559701984ag61ho747nP,N,I,T1559701976958', 'https://oss.max-tv.net.cn/1559701984cha6457mup一拍即盒第一期01_1.jpg', 0, '07:05', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:34:45', '2019-06-05 10:34:45', NULL, 104, 61, '苹果是恶俗文化的带领者（中）', '', 'https://oss.max-tv.net.cn/1559702056pg2z7d18mqS,H,N,T1559702049790', 'https://oss.max-tv.net.cn/1559702055928p1841pq一拍即盒第二期02_1.jpg', 0, '04:49', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:35:36', '2019-06-05 10:35:36', NULL, 105, 61, '苹果是恶俗文化的带领者（下）', '', 'https://oss.max-tv.net.cn/1559702110bt5euj0i5xR,I,V,D1559702103849', 'https://oss.max-tv.net.cn/1559702110m3dbw2l19t一拍即盒第二期03_1.jpg', 0, '08:49', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:39:28', '2019-06-05 10:39:28', NULL, 106, 61, '一拍即盒：双11竞争如此激烈，京东投资人竟放言“咬死它”（上）', '', 'https://oss.max-tv.net.cn/15597022862px1fhhdzhT,O,F,N1559702266094', 'https://oss.max-tv.net.cn/15597022863yl215r1vu一拍即盒第一期01_1.jpg', 0, '07:09', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:40:24', '2019-06-05 10:40:24', NULL, 107, 61, '一拍即盒：双11竞争如此激烈，京东投资人竟放言“咬死它”（中）', '', 'https://oss.max-tv.net.cn/1559702383a7zds3k8n1S,S,C,H1559702367934', 'https://oss.max-tv.net.cn/15597023971io645w8o4一拍即盒第三期02_1.jpg', 0, '06:37', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:41:31', '2019-06-05 10:41:31', NULL, 108, 61, '一拍即盒：双11竞争如此激烈，京东投资人竟放言“咬死它”（下）', '', 'https://oss.max-tv.net.cn/1559702448oyglfrdub8L,B,D,R1559702424118', 'https://oss.max-tv.net.cn/15597024563y98baxfo0一拍即盒第三期03_1.jpg', 0, '08:53', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:46:01', '2019-06-05 10:46:01', NULL, 109, 61, '一拍即盒：200人全都反对，我还是创办了“易到”（上）', '', 'https://oss.max-tv.net.cn/1559702670i76jw1kehbB,O,H,B1559702492335', 'https://oss.max-tv.net.cn/15597026804md47aqqr9一拍即盒第一期01_1.jpg', 0, '06:07', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:47:05', '2019-06-05 10:47:05', NULL, 110, 61, '一拍即盒：200人全都反对，我还是创办了“易到”（中）', '', 'https://oss.max-tv.net.cn/1559702782e9wcpnwl4gV,Y,W,J1559702762217', 'https://oss.max-tv.net.cn/1559702792uzcgx8eq7s一拍即盒第四期02_1.jpg', 0, '04:39', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:48:05', '2019-06-05 10:48:05', NULL, 111, 61, '一拍即盒：200人全都反对，我还是创办了“易到”（下）', '', 'https://oss.max-tv.net.cn/155970284150p5mopdo5W,J,H,X1559702825143', 'https://oss.max-tv.net.cn/1559702849n4p0d6bpgm一拍即盒第四期03_1.jpg', 0, '12:55', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:51:03', '2019-06-05 10:51:03', NULL, 112, 61, '一拍即盒：5G将激活更多科技创新应用（上）', '', 'https://oss.max-tv.net.cn/155970301921qnd2zjcvU,H,L,D1559702930728', 'https://oss.max-tv.net.cn/1559703028y99d2ousd1一拍即盒第一期01_1.jpg', 0, '11:11', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 10:51:57', '2019-06-05 10:51:57', NULL, 113, 61, '一拍即盒第五期：5G将激活更多科技创新应用（下）', '', 'https://oss.max-tv.net.cn/155970307859unx4cpn5F,U,G,H1559703063088', 'https://oss.max-tv.net.cn/1559703086zciuxy8mkt一拍即盒第五期02_1.jpg', 0, '06:21', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 18:39:25', '2019-06-05 18:39:25', NULL, 119, 44, '借力众筹将老房子改为民宿，投资人怎么看？', '', 'https://oss.max-tv.net.cn/1559731066t3srf0cu51Y,L,F,F1559731065077', 'https://oss.max-tv.net.cn/1559731077ijny5i7s0m暖暖的家民宿.jpg', 0, '04:00', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 18:41:29', '2019-06-08 00:35:23', NULL, 120, 44, '跟投已找好，只差领投，投资人怎么说', '', 'https://oss.max-tv.net.cn/1559731243ljr7bi74rmD,Z,R,I1559731200275', 'https://oss.max-tv.net.cn/1559731257jvixsqt7pa译喵智慧翻译云平台.jpg', 4, '05:55', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 18:43:05', '2019-06-08 00:35:19', NULL, 121, 44, '如何向投资人介绍项目才能打动投资人', '', 'https://oss.max-tv.net.cn/1559731326pmvm31rzckY,V,O,O1559731297268', 'https://oss.max-tv.net.cn/1559731357al8ihzst8p童班童学.jpg', 2, '04:42', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 18:44:45', '2019-06-08 00:34:56', NULL, 122, 44, '如何做到“ATM自助存取手机”', '', 'https://oss.max-tv.net.cn/1559731430fgze5dybl8E,C,I,S1559731402317', 'https://oss.max-tv.net.cn/1559731440h5cf57szhp机便利.jpg', 1, '05:54', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 18:52:45', '2019-06-08 00:35:08', NULL, 123, 44, '是什么项目让投资人连连喊到“看不懂”', '', 'https://oss.max-tv.net.cn/1559731649t06pbu0im0F,M,Y,K1559731508017', 'https://oss.max-tv.net.cn/1559731657iw28gyg5xq免录闪学.jpg', 3, '04:49', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-05 18:55:11', '2019-06-05 19:04:01', NULL, 124, 44, '智能珠宝创始人让于光东带他去360踢馆', '', 'https://oss.max-tv.net.cn/155973199700xtbzf2teO,E,R,F1559731968565', 'https://oss.max-tv.net.cn/1559732010djyxrvvgui智能珠宝.jpg', 1, '07:17', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:24:20', '2019-06-10 11:44:26', NULL, 125, 63, 'CEO的秘密|6人游：节奏的精度', '', 'https://oss.max-tv.net.cn/1559787786aut4k1xyr8F,B,R,U1559787671388', 'https://oss.max-tv.net.cn/15597878011i9q7vk6v46人游旅行网.jpg', 1, '00:59', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:26:43', '2019-06-06 10:26:43', NULL, 126, 63, 'CEO的秘密|车萝卜：砸钱做广告不如贴补给用户', '', 'https://oss.max-tv.net.cn/1559787786aut4k1xyr8F,B,R,U1559787671388', 'https://oss.max-tv.net.cn/1559787926zvax2twjh0车萝卜.jpg', 0, '00:59', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:28:25', '2019-06-06 10:28:25', NULL, 127, 63, 'CEO的秘密|触电：为了红，时刻准备着', '', 'https://oss.max-tv.net.cn/1559788014d65a2cd9rjI,Y,W,L1559788007882', 'https://oss.max-tv.net.cn/1559788020v0wgcakeli触电.jpg', 0, '01:28', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:30:15', '2019-06-06 10:30:15', NULL, 128, 63, 'CEO的秘密|光猪圈：企业用人即是与时间赛跑', '', 'https://oss.max-tv.net.cn/1559788124scwrkkx9plT,T,W,C1559788122323', 'https://oss.max-tv.net.cn/1559788133bim7dqlgr6光猪圈.jpg', 0, '01:19', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:31:24', '2019-06-06 10:31:24', NULL, 129, 63, 'CEO的秘密|很快：流量获取是根本', '', 'https://oss.max-tv.net.cn/1559788224c41olommmuK,B,V,X1559788221790', 'https://oss.max-tv.net.cn/1559788231gaomt34jrb很快.jpg', 0, '01:08', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:33:00', '2019-06-06 10:33:00', NULL, 130, 63, 'CEO的秘密|大海盗文化：创业非做不可、非我不可', '', 'https://oss.max-tv.net.cn/1559788287fe5ux0ogkuM,P,D,S1559788285221', 'https://oss.max-tv.net.cn/1559788295c5kirv6nhz老布旅行.jpg', 0, '01:30', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:34:15', '2019-06-06 10:34:15', NULL, 131, 63, 'CEO的秘密|面包求职：投资人更在意宏观问题', '', 'https://oss.max-tv.net.cn/15597883837hylyq7pegU,U,C,J1559788381510', 'https://oss.max-tv.net.cn/1559788390ms51qe56gi面包求职.jpg', 0, '01:33', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:35:30', '2019-06-06 10:35:30', NULL, 132, 63, 'CEO的秘密|木鸟短租：量化焦虑，赋权决策', '', 'https://oss.max-tv.net.cn/1559788459l0nllqwvx5Q,U,M,V1559788456511', 'https://oss.max-tv.net.cn/1559788468n5fqf445y5木鸟短租.jpg', 0, '01:15', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:36:41', '2019-06-06 10:36:41', NULL, 133, 63, 'CEO的秘密|趣学车：用60分服务，博80分效果', '', 'https://oss.max-tv.net.cn/1559788533iop7wiuht3F,D,F,X1559788531077', 'https://oss.max-tv.net.cn/15597885405cl0p3lh59趣学车.jpg', 0, '01:15', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:44:25', '2019-06-06 10:44:25', NULL, 134, 63, 'CEO的秘密|人人湘：做餐饮行业的先驱，不做先烈', '', 'https://oss.max-tv.net.cn/15597886078cag6touyyI,T,T,F1559788605595', 'https://oss.max-tv.net.cn/1559788616ffili9ns2l人人湘.jpg', 0, '01:09', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:46:06', '2019-06-06 10:46:06', NULL, 135, 63, 'CEO的秘密|三个爸爸：移动互联网企业是大趋势', '', 'https://oss.max-tv.net.cn/1559789075akwtjuyyoiH,Z,P,D1559789072037', 'https://oss.max-tv.net.cn/15597890821v27dai3hp三个爸爸.jpg', 0, '01:09', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:49:11', '2019-06-06 10:49:11', NULL, 136, 63, 'CEO的秘密|探探：牺牲男用户？大丈夫！', '', 'https://oss.max-tv.net.cn/1559789171gtbffadwqzB,M,B,F1559789168476', 'https://oss.max-tv.net.cn/1559789181pfnq99il3p探探.jpg', 0, '00:50', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:50:54', '2019-06-06 10:50:54', NULL, 137, 63, 'CEO的秘密|悟空租车：不畏巨头阴影，寻找阳光', '', 'https://oss.max-tv.net.cn/15597893588mk77xlu67W,J,C,Z1559789355452', 'https://oss.max-tv.net.cn/1559789369hoyffl3k56悟空租车.jpg', 0, '01:16', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:52:12', '2019-06-06 10:52:12', NULL, 138, 63, 'CEO的秘密|香橙互动：品牌出名比我出名更重要', '', 'https://oss.max-tv.net.cn/155978946166rh9p3xfdE,Z,X,O1559789458643', 'https://oss.max-tv.net.cn/1559789468e1w5hl2d0s香橙互动.jpg', 0, '01:02', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:53:25', '2019-06-06 10:53:25', NULL, 139, 63, 'CEO的秘密|小旭音乐：小而美与规模化的转折点', '', 'https://oss.max-tv.net.cn/1559789536wv4w20r8veE,S,D,T1559789533811', 'https://oss.max-tv.net.cn/1559789542kznom01sqy小旭音乐.jpg', 0, '01:03', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 10:56:15', '2019-06-06 10:56:15', NULL, 140, 63, 'CEO的秘密|星座不求人：外包拯救大企业病', '', 'https://oss.max-tv.net.cn/1559789608uuit37zkchB,N,G,Q1559789606165', 'https://oss.max-tv.net.cn/1559789614md90eegv64星座不求人.jpg', 0, '01:34', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 14:54:26', '2019-06-08 03:09:09', NULL, 141, 44, '测试测试副标题副标题副标题副标题', '', 'https://oss.max-tv.net.cn/15598040178g65rrfxzyQ,R,Q,X1559803999498', 'https://oss.max-tv.net.cn/1559804056m9et994lq2前台基本功能描述.jpg', 8, '00:59', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 16:52:14', '2019-06-10 11:51:28', NULL, 142, 61, 'ceshi', '', '', '', NULL, '00.59', NULL, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-06 17:39:03', '2019-06-06 17:39:03', NULL, 144, 70, '办公室里的彩虹屁', '', 'https://oss.max-tv.net.cn/1559813838bs9tfjr50nK,T,L,E1559813824513', 'https://oss.max-tv.net.cn/1559813850d7kmflqrgk办公室里的彩虹屁.jpg', 0, '00:59', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-10 11:21:56', '2019-06-10 11:21:56', NULL, 146, 74, '对对对', '', 'https://oss.max-tv.net.cn/15601369019nj9xopc4dI,U,U,I1560136900378', 'https://oss.max-tv.net.cn/1560136914uz8x9jhuxyshhare5.png', 0, '00:59', 0, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-10 12:48:43', '2019-06-10 12:48:46', NULL, 148, 72, '456', NULL, '66', NULL, 8, '00.23', 1, 1);
INSERT INTO `tv_video_info` VALUES ('2019-06-10 12:59:56', '2019-06-10 12:59:56', NULL, 149, 75, '嗯嗯嗯', '', 'https://oss.max-tv.net.cn/1560142782x435fthnqpD,L,V,L1560142780840', 'https://oss.max-tv.net.cn/1560142792ts1yehwfbxshhare6.png', 0, '00:59', 0, 1);

-- ----------------------------
-- Table structure for tv_video_type
-- ----------------------------
DROP TABLE IF EXISTS `tv_video_type`;
CREATE TABLE `tv_video_type`  (
  `create_time` datetime(0) DEFAULT NULL,
  `update_time` datetime(0) DEFAULT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `cross_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `summary_l` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `summary_s` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `summary` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  INDEX `ix_tv_video_type_admin_id`(`admin_id`) USING BTREE,
  INDEX `ix_tv_video_type_status`(`status`) USING BTREE,
  INDEX `ix_tv_video_type_title`(`title`(191)) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 76 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tv_video_type
-- ----------------------------
INSERT INTO `tv_video_type` VALUES ('2019-06-03 14:09:27', '2019-06-06 14:01:37', NULL, 44, '有料的BP 有趣的VC 找项目看这里', 'https://oss.max-tv.net.cn/1559719405hgc5ikyfsq微信图片_20190605152150.jpg', 1, 'https://oss.max-tv.net.cn/1559541955okat2z8nse智见投资百人战.png', NULL, NULL, NULL);
INSERT INTO `tv_video_type` VALUES ('2019-06-04 13:45:57', '2019-06-06 14:01:49', NULL, 58, '洞察产业创新趋势 升级你的人脉圈 ', 'https://oss.max-tv.net.cn/15597075384e0aie68ty大师班.jpg', 1, 'https://oss.max-tv.net.cn/1559627142y0c9rjg04m智见投资大师班-黑底.jpg', NULL, NULL, NULL);
INSERT INTO `tv_video_type` VALUES ('2019-06-04 15:52:02', '2019-06-06 14:02:00', NULL, 59, '带你避开创业路上的那些坑', 'https://oss.max-tv.net.cn/1559634714is0hsyckwk复盘 (2).jpg', 1, 'https://oss.max-tv.net.cn/1559634719v56e9f1ena复盘 (2).jpg', NULL, NULL, NULL);
INSERT INTO `tv_video_type` VALUES ('2019-06-04 15:56:01', '2019-06-05 14:45:30', NULL, 60, 'CEO的秘密', 'https://oss.max-tv.net.cn/1559716740z8bks03dsvCEO的秘密.jpg', 0, 'https://oss.max-tv.net.cn/1559634958lqn8ribshlCEO的秘密.jpg', NULL, NULL, NULL);
INSERT INTO `tv_video_type` VALUES ('2019-06-05 10:05:14', '2019-06-10 12:13:21', NULL, 61, '与投资大咖的脑洞对话', 'https://oss.max-tv.net.cn/15597139798en1tvt81j一拍即盒~1.jpg', 1, 'https://oss.max-tv.net.cn/1559700308y4tm3ahrrs一拍即盒LOGO-黑底.jpg', NULL, NULL, NULL);
INSERT INTO `tv_video_type` VALUES ('2019-06-05 15:26:12', '2019-06-06 14:02:23', NULL, 63, '实力派的方法论', 'https://oss.max-tv.net.cn/15597195625ighkvyrxmCEO的秘密.jpg', 1, 'https://oss.max-tv.net.cn/1559719566e2oal4qf82CEO的秘密.jpg', '', '', '');
INSERT INTO `tv_video_type` VALUES ('2019-06-06 14:18:48', '2019-06-06 14:34:25', NULL, 68, '找对合伙人 没有拿不下的“商战”', 'https://oss.max-tv.net.cn/1559801919msej4sl4ta为梦想加速.jpg', 1, 'https://oss.max-tv.net.cn/1559801921ejqacel5vg为梦想加速.jpg', '找对合伙人 没有拿不下的“商战”', '', '');
INSERT INTO `tv_video_type` VALUES ('2019-06-06 14:33:58', '2019-06-06 14:35:15', NULL, 69, '明星跨界相助 怎么跟投资人”砍价”', 'https://oss.max-tv.net.cn/1559802903s1maoojj04天生我有才.jpg', 1, 'https://oss.max-tv.net.cn/1559801921ejqacel5vg为梦想加速.jpg', '找对合伙人 没有拿不下的“商战”', '', '');
INSERT INTO `tv_video_type` VALUES ('2019-06-06 17:09:06', '2019-06-06 17:26:29', NULL, 70, '梦想靠打拼，皮一下也很开心', 'https://oss.max-tv.net.cn/1559812124f9wm5qh368布斯说.jpg', 1, 'https://oss.max-tv.net.cn/1559812128xqm1lsjvvh布斯说.jpg', '我是立志创业当BOSS的布斯，梦想靠打拼，皮一下也很开心', '', '');
INSERT INTO `tv_video_type` VALUES ('2019-06-06 18:36:57', '2019-06-06 18:36:57', NULL, 71, '创业者说', 'https://oss.max-tv.net.cn/1559817410d4rcwszjoc创业者说.jpg', 1, 'https://oss.max-tv.net.cn/15598174136awr34atpb创业者说.jpg', '创业者说', '', '');
INSERT INTO `tv_video_type` VALUES ('2019-06-10 10:47:23', '2019-06-10 10:47:23', NULL, 72, '测试', 'https://oss.max-tv.net.cn/1560134837ka6l1dqte9shhare3.png', 0, 'https://oss.max-tv.net.cn/1560134839rqkrp5c4qkshhare4.png', '测试分类的简介', '', '');
INSERT INTO `tv_video_type` VALUES ('2019-06-10 11:21:06', '2019-06-10 11:28:34', NULL, 74, '测试1112222', 'https://oss.max-tv.net.cn/1560136876wtz021suk8shhare4.png', 0, 'https://oss.max-tv.net.cn/15601368641tf5ug1977shhare5.png', '测试111122', '', '');
INSERT INTO `tv_video_type` VALUES ('2019-06-10 12:59:03', '2019-06-10 12:59:28', NULL, 75, '测试22', 'https://oss.max-tv.net.cn/1560142736zpfjcraay1shhare5.png', 1, 'https://oss.max-tv.net.cn/15601427383eqa48keevshhare5.png', '测试简介', '', '');

SET FOREIGN_KEY_CHECKS = 1;
