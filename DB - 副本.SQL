CREATE TABLE `t_url_download` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `host_title` varchar(3072) DEFAULT NULL COMMENT '源页面标题',
  `host_url` varchar(3072) DEFAULT NULL COMMENT '源页面地址',
  `title` varchar(3072) DEFAULT NULL COMMENT '子页面标题',
  `url` varchar(3072) DEFAULT NULL COMMENT '子页面地址',
  `url_num` bigint(255) DEFAULT NULL COMMENT '子页面地址计数',,
  `state_flag` tinyint(255) DEFAULT '0' COMMENT '爬取状态 ：1-已爬取 0-未爬取 ',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;



CREATE TABLE `t_img_download` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `url_id` bigint(255) DEFAULT NULL,
  `host_title` varchar(3072) DEFAULT NULL COMMENT '源页面标题',
  `host_url` varchar(3072) DEFAULT NULL COMMENT '源页面地址',
  `img_web_title` varchar(3072) DEFAULT NULL COMMENT '子页面标题',
  `img_url` varchar(3072) DEFAULT NULL COMMENT '图片爬取地址',
  `img_num` bigint(255) DEFAULT NULL COMMENT '图片爬取地址计数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

