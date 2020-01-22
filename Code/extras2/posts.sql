create table Posts(
	Id int,
	PostTypeId tinyint,
	AcceptedAnswerId int,
	ParentId int,
	CreationDate datetime,
	DeletionDate datetime,
	Score int,
	ViewCount int,
	Body varchar (250),
	OwnerUserId int,
	OwnerDisplayName varchar (40),
	LastEditorUserId int,
	LastEditorDisplayName varchar (40),
	LastEditDate datetime,
	LastActivityDate datetime,
	Title varchar (250),
	Tags varchar (250),
	AnswerCount int,
	CommentCount int,
	FavoriteCount int,
	ClosedDate datetime,
	CommunityOwnedDate datetime
);

LOAD XML LOCAL INFILE '/media/adesh/ACB68A5CB68A26C4/btp/dump/java_posts_1lac_clean.xml' INTO TABLE Posts; 

-- select Id, OwnerUserId, AcceptedAnswerId,  into temp_table
-- from Posts where PostTypeId = 2;