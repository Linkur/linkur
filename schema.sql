
-- Schema: public

DROP SCHEMA public;

CREATE SCHEMA public
  AUTHORIZATION postgres;

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public
  IS 'standard public schema';

-- Table: users

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
  id uuid NOT NULL, -- uuid - user_id
  name character varying NOT NULL, -- user name
  email character varying NOT NULL, -- user email
  password character(46), -- encrypted password
  CONSTRAINT user_pk PRIMARY KEY (id),
  CONSTRAINT user_uk UNIQUE (email)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE users
  OWNER TO linkur;
COMMENT ON TABLE users
  IS 'users table';
COMMENT ON COLUMN users.id IS 'uuid - user_id';
COMMENT ON COLUMN users.name IS 'user name';
COMMENT ON COLUMN users.email IS 'user email';
COMMENT ON COLUMN users.password IS 'encrypted password';


-- Table: groups

DROP TABLE IF EXISTS groups;

CREATE TABLE groups
(
  id uuid NOT NULL, -- group id
  title character varying, -- title for group
  CONSTRAINT group_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE groups
  OWNER TO linkur;
COMMENT ON TABLE groups
  IS 'groups table';
COMMENT ON COLUMN groups.id IS 'group id';
COMMENT ON COLUMN groups.title IS 'title for group';


-- Table: posts

DROP TABLE IF EXISTS posts;

CREATE TABLE posts
(
  id uuid NOT NULL, -- id for post. uuid for uniqueness
  title character varying(255),
  link character varying,
  group_id uuid NOT NULL, -- group to which post belongs
  added_by uuid NOT NULL, -- user who added the post
  tags character varying(255)[] DEFAULT '{}'::character varying[], -- tags of post, if any
  date timestamp with time zone, -- time stamp
  CONSTRAINT post_pk PRIMARY KEY (id),
  CONSTRAINT post_group_fk FOREIGN KEY (added_by)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT post_user_fk FOREIGN KEY (added_by)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE posts
  OWNER TO linkur;
COMMENT ON TABLE posts
  IS 'posts table';
COMMENT ON COLUMN posts.id IS 'id for post. uuid for uniqueness';
COMMENT ON COLUMN posts.group_id IS 'group to which post belongs';
COMMENT ON COLUMN posts.added_by IS 'user who added the post';
COMMENT ON COLUMN posts.tags IS 'tags of post, if any';
COMMENT ON COLUMN posts.date IS 'time stamp';


-- Table: user_groups

DROP TABLE IF EXISTS user_groups;

CREATE TABLE user_groups
(
  user_id uuid NOT NULL, -- user_id
  group_id uuid NOT NULL, -- group_id
  CONSTRAINT usergroups_pk PRIMARY KEY (user_id, group_id),
  CONSTRAINT usergroups_group_fk FOREIGN KEY (group_id)
      REFERENCES groups (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT usergroups_user_fk FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE user_groups
  OWNER TO linkur;
COMMENT ON TABLE user_groups
  IS 'User subscribed group';
COMMENT ON COLUMN user_groups.user_id IS 'user_id';
COMMENT ON COLUMN user_groups.group_id IS 'group_id';


-- Table: user_reading_list

DROP TABLE IF EXISTS user_reading_list;

CREATE TABLE user_reading_list
(
  user_id uuid NOT NULL, -- user id
  post_id uuid NOT NULL, -- post id
  status int2vector, -- status codes for read, starred etc
  CONSTRAINT user_readinglist_pk PRIMARY KEY (user_id, post_id),
  CONSTRAINT user_readinglist_post_fk FOREIGN KEY (post_id)
      REFERENCES posts (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT user_readinglist_user_fk FOREIGN KEY (user_id)
      REFERENCES users (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE user_reading_list
  OWNER TO linkur;
COMMENT ON TABLE user_reading_list
  IS 'unarchived posts for user';
COMMENT ON COLUMN user_reading_list.user_id IS 'user id';
COMMENT ON COLUMN user_reading_list.post_id IS 'post id';
COMMENT ON COLUMN user_reading_list.status IS 'status codes for read, starred etc';


-- View: vw_user_posts

DROP VIEW IF EXISTS vw_user_posts;

CREATE OR REPLACE VIEW vw_user_posts AS 
 SELECT p.id,
    p.title,
    p.link,
    p.group_id,
    p.added_by,
    p.date,
    p.tags
   FROM user_reading_list rl
   JOIN posts p ON rl.post_id = p.id AND (p.group_id IN ( SELECT user_groups.group_id
      FROM user_groups
     WHERE user_groups.user_id = rl.user_id));

ALTER TABLE vw_user_posts
  OWNER TO linkur;
COMMENT ON VIEW vw_user_posts
  IS 'View for user_reading_list join posts table';

