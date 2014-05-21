--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.4
-- Dumped by pg_dump version 9.3.4
-- Started on 2014-05-21 22:38:35 IST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE linkur;
--
-- TOC entry 2029 (class 1262 OID 16393)
-- Name: linkur; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE linkur WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_IN' LC_CTYPE = 'en_IN';


\connect linkur

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 6 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- TOC entry 2030 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 176 (class 3079 OID 11791)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2031 (class 0 OID 0)
-- Dependencies: 176
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 177 (class 3079 OID 16394)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 2032 (class 0 OID 0)
-- Dependencies: 177
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET search_path = public, pg_catalog;

SET default_with_oids = false;

--
-- TOC entry 170 (class 1259 OID 16405)
-- Name: groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE groups (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    title character varying
);


--
-- TOC entry 2033 (class 0 OID 0)
-- Dependencies: 170
-- Name: TABLE groups; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE groups IS 'groups table';


--
-- TOC entry 2034 (class 0 OID 0)
-- Dependencies: 170
-- Name: COLUMN groups.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN groups.id IS 'group id';


--
-- TOC entry 2035 (class 0 OID 0)
-- Dependencies: 170
-- Name: COLUMN groups.title; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN groups.title IS 'title for group';


--
-- TOC entry 173 (class 1259 OID 40979)
-- Name: posts; Type: TABLE; Schema: public; Owner: -
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


--
-- TOC entry 2036 (class 0 OID 0)
-- Dependencies: 173
-- Name: TABLE posts; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE posts IS 'posts table';


--
-- TOC entry 2037 (class 0 OID 0)
-- Dependencies: 173
-- Name: COLUMN posts.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN posts.id IS 'id for post. uuid for uniqueness';


--
-- TOC entry 2038 (class 0 OID 0)
-- Dependencies: 173
-- Name: COLUMN posts.group_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN posts.group_id IS 'group to which post belongs';


--
-- TOC entry 2039 (class 0 OID 0)
-- Dependencies: 173
-- Name: COLUMN posts.added_by; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN posts.added_by IS 'user who added the post';


--
-- TOC entry 2040 (class 0 OID 0)
-- Dependencies: 173
-- Name: COLUMN posts.tags; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN posts.tags IS 'tags of post, if any';


--
-- TOC entry 2041 (class 0 OID 0)
-- Dependencies: 173
-- Name: COLUMN posts.date; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN posts.date IS 'time stamp';


--
-- TOC entry 174 (class 1259 OID 49161)
-- Name: user_archived_posts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE user_archived_posts (
    user_id uuid NOT NULL,
    post_id uuid NOT NULL
);


--
-- TOC entry 2042 (class 0 OID 0)
-- Dependencies: 174
-- Name: COLUMN user_archived_posts.user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN user_archived_posts.user_id IS 'user id';


--
-- TOC entry 2043 (class 0 OID 0)
-- Dependencies: 174
-- Name: COLUMN user_archived_posts.post_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN user_archived_posts.post_id IS 'post id';


--
-- TOC entry 171 (class 1259 OID 16420)
-- Name: user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE user_groups (
    user_id uuid NOT NULL,
    group_id uuid NOT NULL
);


--
-- TOC entry 2044 (class 0 OID 0)
-- Dependencies: 171
-- Name: TABLE user_groups; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE user_groups IS 'User subscribed group';


--
-- TOC entry 2045 (class 0 OID 0)
-- Dependencies: 171
-- Name: COLUMN user_groups.user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN user_groups.user_id IS 'user_id';


--
-- TOC entry 2046 (class 0 OID 0)
-- Dependencies: 171
-- Name: COLUMN user_groups.group_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN user_groups.group_id IS 'group_id';


--
-- TOC entry 172 (class 1259 OID 16426)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE users (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    password character(98)
);


--
-- TOC entry 2047 (class 0 OID 0)
-- Dependencies: 172
-- Name: TABLE users; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE users IS 'users table';


--
-- TOC entry 2048 (class 0 OID 0)
-- Dependencies: 172
-- Name: COLUMN users.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN users.id IS 'uuid - user_id';


--
-- TOC entry 2049 (class 0 OID 0)
-- Dependencies: 172
-- Name: COLUMN users.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN users.name IS 'user name';


--
-- TOC entry 2050 (class 0 OID 0)
-- Dependencies: 172
-- Name: COLUMN users.email; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN users.email IS 'user email';


--
-- TOC entry 2051 (class 0 OID 0)
-- Dependencies: 172
-- Name: COLUMN users.password; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN users.password IS 'encrypted password';


--
-- TOC entry 175 (class 1259 OID 49192)
-- Name: vw_user_posts; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW vw_user_posts AS
 SELECT p.id,
    p.title,
    p.link,
    p.group_id,
    p.added_by,
    p.date,
    p.tags,
    ug_1.user_id
   FROM (posts p
   JOIN user_groups ug_1 ON (((p.group_id = ug_1.group_id) AND (NOT ((p.id, ug_1.user_id) IN ( SELECT uap.post_id AS id,
       uap.user_id
      FROM (user_archived_posts uap
   JOIN user_groups ug_2 ON ((uap.user_id = ug_2.user_id)))))))))
  ORDER BY ug_1.user_id;


--
-- TOC entry 1900 (class 2606 OID 16438)
-- Name: group_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT group_pk PRIMARY KEY (id);


--
-- TOC entry 1908 (class 2606 OID 40988)
-- Name: post_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT post_pk PRIMARY KEY (id);


--
-- TOC entry 1904 (class 2606 OID 16442)
-- Name: user_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT user_pk PRIMARY KEY (id);


--
-- TOC entry 1910 (class 2606 OID 49165)
-- Name: user_post_archive_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_archived_posts
    ADD CONSTRAINT user_post_archive_pk PRIMARY KEY (user_id, post_id);


--
-- TOC entry 1906 (class 2606 OID 16446)
-- Name: user_uk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT user_uk UNIQUE (email);


--
-- TOC entry 1902 (class 2606 OID 16448)
-- Name: usergroups_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT usergroups_pk PRIMARY KEY (user_id, group_id);


--
-- TOC entry 1913 (class 2606 OID 40989)
-- Name: post_group_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT post_group_fk FOREIGN KEY (group_id) REFERENCES groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1914 (class 2606 OID 40994)
-- Name: post_user_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT post_user_fk FOREIGN KEY (added_by) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1916 (class 2606 OID 49171)
-- Name: user_posts_archive_post_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_archived_posts
    ADD CONSTRAINT user_posts_archive_post_fk FOREIGN KEY (post_id) REFERENCES posts(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1915 (class 2606 OID 49166)
-- Name: user_posts_archive_user_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_archived_posts
    ADD CONSTRAINT user_posts_archive_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1911 (class 2606 OID 16469)
-- Name: usergroups_group_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT usergroups_group_fk FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;


--
-- TOC entry 1912 (class 2606 OID 16474)
-- Name: usergroups_user_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_groups
    ADD CONSTRAINT usergroups_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


-- Completed on 2014-05-21 22:38:35 IST

--
-- PostgreSQL database dump complete
--

