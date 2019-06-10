create table User
(
    username VARCHAR(25) not null,
    passwd VARCHAR(40) not null,
    primary key(username)
)
;
create table Blog
(
	blogid INT(10) auto_increment ,
    title varchar(40) not null,
    author varchar(25) not null, # as same as User's username
    content text(1000) default null,
    sub_date varchar(50),
    primary key (blogid)
)
;
create table BlogComment
(
	commentid INT(10) auto_increment,
    blogid INT(10) not null,
    author varchar(25) not null, # as same as User's username
    content text(1000) default null,
    sub_date varchar(50),
    primary key (commentid)
)