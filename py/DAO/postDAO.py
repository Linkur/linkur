__author__ = 'raghothams'

from model.post import Post
import datetime
from bson import ObjectId

class PostDAO:

    def __init__(self, database):
        self.db = database
        self.recent_collection = self.db.new
        self.achived_collection = self.db.archive

    def get_recent_posts(self, groupid):
        
        posts = None
        try:
            groupid = ObjectId(groupid)
            collection = self.recent_collection
            posts = collection.find({
                'group' : groupid
                })
            print 'posts - ', posts
        except Exception as inst:
            print "error reading recent posts"
            print inst

        if posts != None:
            post_list = self.get_modelled_list(posts)
            print 'LOL'
            print post_list
            return post_list
        else:
            return None

    def get_archived_posts(self, groupid):

        posts = None
        try:
            groupid = ObjectId(groupid)
            collection = self.achived_collection
            posts = collection.find({
                'group' : groupid
                })

        except Exception as inst:
            print "error reading recent posts"
            print inst

        if posts != None:
            post_list = self.get_modelled_list(posts)
            return post_list
        else:
            return None

    def searchCollection(self, groups, collection, queryTexts):
        modelled_search_results = None
        
        query_string = []

        # build query based on the search strings
        for query in queryTexts:
            # check for title field
            interim_string = {"title":query}
            query_string.append(interim_string)

            # check if string is part of tags array
            interim_string = {"tags":{"$in":[query]}}
            query_string.append(interim_string)

        # and group
        group_query = []
        for group in groups:
            interim_clause = {"group":group["_id"]}
            group_query.append(interim_clause)
        group_query = [{"$or":group_query}]

        query_string = {"$or":query_string, "$and":group_query}

        print query_string
            # print query
        try:
            results = collection.find(
                query_string                
                )

            if results != None:
                intermediate_result = self.get_modelled_list(results)
                print "interim result", intermediate_result
                if modelled_search_results == None:
                    modelled_search_results = intermediate_result
                else:
                    modelled_search_results = modelled_search_results + intermediate_result

        except Exception as inst:
            print "error processing search"
            print inst
            return None
        print "final result title", modelled_search_results
        return modelled_search_results
        

    def search(self, user, queryText):
        posts = None
        queryText = queryText.split(',')
        
        # find the groups user belongs to and pass groups array as a param to searchCollection
        groups = user.groups
        
        title_results = self.searchCollection(groups, self.recent_collection, queryText)
        if title_results != None:
            posts = title_results
        
        title_results = self.searchCollection(groups, self.achived_collection, queryText)
        
        if title_results != None:
            if posts != None:
                posts = posts + title_results
            else:
                posts = title_results

        return posts

    def get_modelled_list(self, posts):

        modelled_post_list = []
        for post in posts:
            try:
                modelled_post = Post()
                modelled_post.id = post['_id']

                date_obj = post['date']
                modelled_post.date = date_obj.isoformat()
                # print post['title']
                modelled_post.title = post['title']
                modelled_post.link = post['link']
                modelled_post.category = post['category']
                modelled_post.tags = post['tags']
                modelled_post.group = post['group']
                modelled_post.added_by = post['added_by']
                # print modelled_post.title
                modelled_post_list.append(modelled_post)
                # print "in", modelled_post_list

            except Exception as inst:
                print "error processing objects"
                print inst
                return None
        # print "out", modelled_post_list
        return modelled_post_list

    def insert_post(self, post_obj):

        collection = self.recent_collection
        result = None
        try:
            to_insert = post_obj.db_serializer()
            # print to_insert
            result = collection.insert(to_insert)
        except Exception as inst:
            print "error writing post"
            print inst

        return result

    def delete_post(self, post_id):

        collection = self.recent_collection
        result = None
        
        try:
            to_delete = {"_id":ObjectId(post_id)}
            print "to delete is ", to_delete
            
            result = collection.remove(to_delete, safe=True)

        except Exception as inst:
            print "error removing post"
            print inst

        return result

    def update_post(self, post_obj):

        collection = self.recent_collection
        result = None
        
        try:
            update_what = {"_id":ObjectId(post_obj.id)}
            to_update = post_obj.db_serializer()
            print "you are about to upadate the post and this is the data given"
            print to_update
            result = collection.update(update_what,to_update, upsert=False, safe=True)

        except Exception as inst:
            print "error updating post"
            print inst
            return False

        return result

