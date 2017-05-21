# ProxyPool 代理IP池

## Feature 特点
* 抓取国内外代理IP站点，并通过访问httpbin判断是否透明\高匿，连通时间，IP地区等信息
* 自动检测入库IP是否存活，会有20次存活期，若在检测过程中，超过了20次检测期还没有连通，则自动出库
* 提供API


ProxyPool 分为三个部分： **Spider** ， **Process**， **WebService**

### Spider
爬取IP地址，判断IP地址有效性，连通率及支持类型，最后判断数据库中是否已存在该IP，若不存在则入库

### Process
无限期从表中取出IP，默认开启两个线程（可在```config.conf```中设置线程数），线程**1**永远取前20个已较长时间没有做验证的IP，其余线程会去取没有做过验证的IP地址

### WebService
基于Flask RESTful为客户提供API调用
默认：**http://127.0.0.1/api/getProxy** 取出活着的且速度从快到慢前5个IP地址

可为上述地址添加下列参数：

参数名 | 参数名（中文） | eg | 备注 |
------ | ----------- | ---- | --- |
https | 是否需要支持https | https=1 | 取出支持https的ip
type | 代理ip类型 | type = 0 | 透明代理：type=0，匿名代理：type=1，高匿代理：type=2
country | 代理IP地区 | country=国内 | country=国内，目前仅支持***国内or国外***，国内代表中国大陆，国外代表除中国大陆外
count | 取出数量 | count=15 | 取出代理IP数量，默认为5个，上限为20个

eg: **http://127.0.0.1/api/getProxy?https=1&type=2&country=国内&count=15**

## Python Version Python版本
`python 3.* `
## Import 依赖包

* Flask
* PyQuery
* PIL
* aiohttp
* asyncio
* requests
* configparser
* pymysql


## Database 数据库
默认使用mysql，数据库表（表名为httpbin）结构如下（附建表语句）：


字段名 | 字段名（中文） |  类型 | 备注
------ | ----------- | ----- | ----- |
id | 主键 | int(11) |
ip | ip地址 | varchar | ip地址
port | 端口 | varchat | ip端口
https | 是否支持https | int | 支持：1，不支持：0
anonymity | 代理类型 | int | 透明：0，匿名：1，高匿2
country | 所属国家（地区） | varchar(20) | 所属国家（地区）
speed | 连通时间 | varchar | 连通时间，单位：秒
source | 来源站点 | varchar | 来源站点
alive | 是否存活 | varchar | 存活：1，死亡：0
insert_time | 入库时间 | datetime | 第一次插入数据库时间
update_time | 验证更新时间 | datetime | 最近一次验证时间
used_count | 使用次数 | int | 被API调用次数
verify_count | 累计验证次数 | int | 累计验证次数
leave_count | 具体删除次数 | int | 初始20，每失败一次 -1，直到为0时从库中删除


建表语句如下：

```

create table httpbin
(
	id int auto_increment
		primary key,
	ip varchar(50) not null,
	port varchar(20) not null,
	https int null comment '是否支持https（支持：1，不支持：0）',
	anonymity int null comment '代理类型（透明：0，匿名：1，高匿：2）',
	country varchar(20) null comment '所属国家',
	speed varchar(50) null comment '连通时间（单位：秒）',
	source varchar(50) null comment '来源站点',
	alive varchar(10) default '1' null comment '该ip是否有效（验证通过：true(1)，验证不通过：false(0)）',
	insert_time datetime null comment '第一次插入时间',
	update_time datetime null comment '验证更新时间',
	used_count int default '0' null comment '在代理池中已使用次数',
	verify_count int default '1' null comment '已累计验证次数',
	leave_count int default '20' null comment '距离删除次数（初始20次）'
)
;


```

