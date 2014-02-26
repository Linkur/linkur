--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.user_groups DROP CONSTRAINT usergroups_user_fk;
ALTER TABLE ONLY public.user_groups DROP CONSTRAINT usergroups_group_fk;
ALTER TABLE ONLY public.user_reading_list DROP CONSTRAINT user_readinglist_user_fk;
ALTER TABLE ONLY public.user_reading_list DROP CONSTRAINT user_readinglist_post_fk;
ALTER TABLE ONLY public.posts DROP CONSTRAINT post_user_fk;
ALTER TABLE ONLY public.posts DROP CONSTRAINT post_group_fk;
ALTER TABLE ONLY public.user_groups DROP CONSTRAINT usergroups_pk;
ALTER TABLE ONLY public.users DROP CONSTRAINT user_uk;
ALTER TABLE ONLY public.user_reading_list DROP CONSTRAINT user_readinglist_pk;
ALTER TABLE ONLY public.users DROP CONSTRAINT user_pk;
ALTER TABLE ONLY public.posts DROP CONSTRAINT post_pk;
ALTER TABLE ONLY public.groups DROP CONSTRAINT group_pk;
DROP VIEW public.vw_user_posts;
DROP TABLE public.users;
DROP TABLE public.user_reading_list;
DROP TABLE public.user_groups;
DROP TABLE public.posts;
DROP TABLE public.groups;
DROP EXTENSION "uuid-ossp";
DROP EXTENSION plpgsql;
DROP SCHEMA public;
DROP DATABASE IF EXISTS linkur;

-- Database: linkur

CREATE DATABASE linkur;

\connect linkur;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE groups (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    title character varying
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- Name: TABLE groups; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE groups IS 'groups table';


--
-- Name: COLUMN groups.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN groups.id IS 'group id';


--
-- Name: COLUMN groups.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN groups.title IS 'title for group';


--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE posts (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    title character varying(255),
    link character varying,
    group_id uuid NOT NULL,
    added_by uuid NOT NULL,
    tags character varying(255)[] DEFAULT '{}'::character varying[],
    date timestamp with time zone
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: TABLE posts; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE posts IS 'posts table';


--
-- Name: COLUMN posts.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN posts.id IS 'id for post. uuid for uniqueness';


--
-- Name: COLUMN posts.group_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN posts.group_id IS 'group to which post belongs';


--
-- Name: COLUMN posts.added_by; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN posts.added_by IS 'user who added the post';


--
-- Name: COLUMN posts.tags; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN posts.tags IS 'tags of post, if any';


--
-- Name: COLUMN posts.date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN posts.date IS 'time stamp';


--
-- Name: user_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE user_groups (
    user_id uuid NOT NULL,
    group_id uuid NOT NULL
);


ALTER TABLE public.user_groups OWNER TO postgres;

--
-- Name: TABLE user_groups; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE user_groups IS 'User subscribed group';


--
-- Name: COLUMN user_groups.user_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN user_groups.user_id IS 'user_id';


--
-- Name: COLUMN user_groups.group_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN user_groups.group_id IS 'group_id';


--
-- Name: user_reading_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE user_reading_list (
    user_id uuid NOT NULL,
    post_id uuid NOT NULL,
    status int2vector
);


ALTER TABLE public.user_reading_list OWNER TO postgres;

--
-- Name: TABLE user_reading_list; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE user_reading_list IS 'unarchived posts for user';


--
-- Name: COLUMN user_reading_list.user_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN user_reading_list.user_id IS 'user id';


--
-- Name: COLUMN user_reading_list.post_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN user_reading_list.post_id IS 'post id';


--
-- Name: COLUMN user_reading_list.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN user_reading_list.status IS 'status codes for read, starred etc';


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    password character(98)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: TABLE users; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE users IS 'users table';


--
-- Name: COLUMN users.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN users.id IS 'uuid - user_id';


--
-- Name: COLUMN users.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN users.name IS 'user name';


--
-- Name: COLUMN users.email; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN users.email IS 'user email';


--
-- Name: COLUMN users.password; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN users.password IS 'encrypted password';


--
-- Name: vw_user_posts; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW vw_user_posts AS
 SELECT p.id,
    p.title,
    p.link,
    p.group_id,
    p.added_by,
    p.date,
    p.tags
   FROM (user_reading_list rl
   JOIN posts p ON (((rl.post_id = p.id) AND (p.group_id IN ( SELECT user_groups.group_id
      FROM user_groups
     WHERE (user_groups.user_id = rl.user_id))))));


ALTER TABLE public.vw_user_posts OWNER TO postgres;

--
-- Name: VIEW vw_user_posts; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW vw_user_posts IS 'View for user_reading_list join posts table';


--
-- Name: group_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT group_pk PRIMARY KEY (id);


--
-- Name: post_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT post_pk PRIMARY KEY (id);


--
-- Name: user_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT user_pk PRIMARY KEY (id);


--
-- Name: user_readinglist_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY user_reading_list
    ADD CONSTRAINT user_readinglist_pk PRIMARY KEY (user_id, post_id);


--
-- Name: user_uk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT user_uk UNIQUE (email);


--
-- Name: usergroups_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT usergroups_pk PRIMARY KEY (user_id, group_id);


--
-- Name: post_group_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT post_group_fk FOREIGN KEY (group_id) REFERENCES groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: post_user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT post_user_fk FOREIGN KEY (added_by) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_readinglist_post_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_reading_list
    ADD CONSTRAINT user_readinglist_post_fk FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE;


--
-- Name: user_readinglist_user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_reading_list
    ADD CONSTRAINT user_readinglist_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: usergroups_group_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT usergroups_group_fk FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;


--
-- Name: usergroups_user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT usergroups_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

