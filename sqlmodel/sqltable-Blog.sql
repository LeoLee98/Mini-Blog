create schema Blog;
use Blog;
create table User
(
    userid INT(10) auto_increment,
    username VARCHAR(25) not null,
    passwd VARCHAR(40) not null,
    primary key(userid),
)
engine = InnoDB
;
create table Blog
(
	blogid INT(10) auto_increment ,
    title varchar(40) not null,
    author varchar(25) not null, # as same as User's usernameBlogUser
    content text(1000) default null,
    comment_num INT(11) default 0,
	sub_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  ON UPDATE CURRENT_TIMESTAMP,
    primary key (blogid)
    INDEX(author)
)
engine = InnoDB
;
create table BlogComment
(
	commentid INT(10) auto_increment,
    blogid INT(10) not null,
    author varchar(25) not null, # as same as User's username
    content text(1000) default null,
    sub_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  ON UPDATE CURRENT_TIMESTAMP,
    primary key (commentid)
    INDEX(blogid)
)
engine = InnoDB
;