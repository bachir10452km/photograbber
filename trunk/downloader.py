import os, re, sys, urllib2, time
from threading import Thread

class FBDownloader(Thread):
    REPLACE_RE = re.compile(r'\*|"|\'|:|<|>|\?|\\|/|\|,| ')
    CAPTION = -1
    DESCRIPTION = -2
    LOCATION = -3

    def __init__ (self, photos_path, uid, friends,
                        full_albums, user_albums, extras, facebook,
                        update_callback, error_callback, force_exit_callback):
        Thread.__init__(self)
        self.photos_path = photos_path
        self.uid = uid
        self.friends = friends
        self.facebook = facebook
        # options
        self.full_albums = full_albums
        self.user_albums = user_albums
        self.extras = extras
        # callback functions
        self.update = update_callback
        self.error = error_callback
        self.force_exit = force_exit_callback

        self._thread_terminated = False
        self.index = self.total = 0
        self.albums = {}        # hold all pic data

    def retry_function(self, max_retries, function, *args, **kw):
        retries = 0
        while True:
            self.exit_if_terminated()
            try:
                return function(*args, **kw)
            except Exception, e:
                if retries < max_retries:
                    self.error('retrying function: %d\n' % retries, False)
                    retries += 1
                    # sleep longer and longer between retries
                    time.sleep(retries * 2)
                else:
                    raise

    # terminate the thread if need be
    def exit_if_terminated(self):
        if self._thread_terminated:
            sys.exit() # raise SystemExit exception to terminate run()

    # queries fail a lot, lets retry them too
    def query_wrapper(self, q):
        try:
            return self.retry_function(10, self.facebook.fql.query, q)
        except Exception, e:
            # maybe do something different with error...
            self.error(e)

    # return a persons name
    def friend_name(self, uid):
        if uid == None:
            # this should never happen... but it did once
            return 'Unknown'
        if uid not in self.friends:
            q = 'SELECT name FROM profile WHERE id=%s'
            res = self.query_wrapper(q % uid)
            if res:
                self.friends[uid] = res[0]['name']
            else:
                self.friends[uid] = 'uid_%s' % uid # could not find real name
        return self.friends[uid]

    # functions to write extra info

    def write_comments(self, filename, comments):
        fp = open(filename, 'w')
        for comment in sorted(comments, key=lambda x:x['time']):
            if comment['fromid'] == self.CAPTION:
                fp.write('Photo Caption\n')
            elif comment['fromid'] == self.DESCRIPTION:
                fp.write('Album Description\n')
            elif comment['fromid'] == self.LOCATION:
                fp.write('Album Location\n')
            else:
                friend = self.friend_name(comment['fromid'])
                fp.write('%s ' % time.ctime(int(comment['time'])))
                fp.write('%s\n' % friend.encode('utf-8'))
            fp.write('%s\n\n' % comment['text'].encode('utf-8'))
        fp.close()
        os.utime(filename, (int(comment['time']),) * 2)

    def write_tags(self, filename, tags, file_time):
        fp = open(filename, 'w')
        for tag in sorted(tags, key=lambda x:(float(x['xcoord']),
                                              float(x['ycoord']))):
            fp.write('%9.5f %9.5f %s\n' % (tag['xcoord'], tag['ycoord'],
                                           tag['text'].encode('utf-8')))
        fp.close()
        os.utime(filename, (file_time,) * 2)


    # get albums and photos
    # heavy FQL statements

    def get_albums(self):
        # all albums the user is tagged in
        q = ''.join(['SELECT aid, owner, name, modified, description, ',
                     'location, object_id FROM album WHERE aid IN (SELECT ',
                     'aid FROM photo WHERE pid IN (SELECT pid FROM photo_tag ',
                     'WHERE subject="%s"))']) % self.uid

        for item in self.query_wrapper(q):
            item['photos'] = {}
            self.albums[item['aid']] = item


        # all albums uploaded by the user
        q = ''.join(['SELECT aid, owner, name, modified, description, ',
                     'location, object_id FROM album WHERE ',
                     'owner="%s"']) % self.uid
        if self.user_albums:
            for item in self.query_wrapper(q):
                item['photos'] = {}
                self.albums[item['aid']] = item

    def get_pictures(self):
        # all pictures where the user is tagged
        q = ''.join(['SELECT pid, aid, src_big, caption, created, object_id ',
                     'FROM photo WHERE pid IN (SELECT pid FROM photo_tag ',
                     'WHERE subject="%s")']) % self.uid

        if self.full_albums:
            # full albums where the user is tagged
            q = ''.join(['SELECT pid, aid, src_big, caption, created, ',
                         'object_id FROM photo WHERE aid IN (SELECT aid ',
                         'FROM photo WHERE pid IN (SELECT pid FROM photo_tag ',
                         'WHERE subject="%s"))']) % self.uid

        for photo in self.query_wrapper(q):
            self.albums[photo['aid']]['photos'][photo['pid']] = photo

        if self.user_albums:
            # all pictures in albums uploaded by the user
            q = ''.join(['SELECT pid, aid, src_big, caption, created, ',
                         'object_id FROM photo WHERE aid IN (SELECT aid FROM ',
                         'album WHERE owner="%s")']) % self.uid
            for photo in self.query_wrapper(q):
                self.albums[photo['aid']]['photos'][photo['pid']] = photo

    # yay
    def save_album(self, album):
        self.exit_if_terminated()

        # get album and photo comments
        q = ''.join(['SELECT object_id, fromid, time, text FROM comment ',
                     'WHERE object_id in (%s)'])

        o2pid = {} # translate object_id to pid
        oids = [] # hold object_ids to lookup

        album_comments = []

        for photo in album['photos'].values():
            o2pid[photo['object_id']] = photo['pid']
            oids.append('"%s"' % photo['object_id'])
            if photo['caption']:
                photo['comments'] = [{'fromid':self.CAPTION,
                                      'text':photo['caption'], 'time':0}]

        oids.append('"%s"' % album['object_id'])
        if album['description']:
            album_comments.append({'fromid':self.DESCRIPTION, 'time':0,
                                   'text':album['description']})
        if album['location']:
            album_comments.append({'fromid':self.LOCATION, 'time':1,
                                   'text':album['location']})

        # do i want extra info?
        if self.extras:
            # load all comments for album and its photos
            for item in self.query_wrapper(q % ','.join(oids)):
                oid = item['object_id']
                if oid in o2pid: # photo comment
                    clist = album['photos'][o2pid[oid]].setdefault('comments',
                                                                   [])
                    clist.append(item)
                else: # album comment
                    album_comments.append(item)

            # load tags in each photo
            q = ''.join(['SELECT pid, text, xcoord, ycoord FROM ',
                         'photo_tag WHERE pid IN(%s)'])
            pids = ['"%s"' % x for x in album['photos'].keys()]
            for item in self.query_wrapper(q % ','.join(pids)):
                tag_list = album['photos'][item['pid']].setdefault('tags', [])
                tag_list.append(item)

        username = self.friend_name(album['owner'])
        album_folder = self.REPLACE_RE.sub(
                '_', '%s-%s' % (username, album['name']))
        album_path = os.path.join(self.photos_path, album_folder)

        # Create album directory if it doesn't exist
        if not os.path.isdir(album_path):
            os.mkdir(album_path)

        # Save album comments
        if album_comments:
            meta_path = os.path.join(album_path, 'ALBUM_COMMENTS.txt')
            self.write_comments(meta_path, album_comments)

        for photo in album['photos'].items():
            # update progress bar
            self.update(self.index, self.total)
            self.index += 1
            # save photo
            self.save_photo(album_path, *photo)

        # Reset modify time after adding files
        os.utime(album_path, (int(album['modified']),) * 2)


    def save_photo(self, album_path, pid, photo):
        self.exit_if_terminated()

        filename = os.path.join(album_path, '%s.jpg' % pid)
        if 'comments' in photo:
            meta_name = os.path.join(album_path, '%s_comments.txt' % pid)
            self.write_comments(meta_name, photo['comments'])

        if 'tags' in photo:
            meta_name = os.path.join(album_path, '%s_tags.txt' % pid)
            self.write_tags(meta_name, photo['tags'], int(photo['created']))

        # If file already exists don't download
        if os.path.isfile(filename): return

        # skip on 404 error: Issue 13
        try:
            picout = open(filename, 'wb')
            handler = urllib2.Request(photo['src_big'])
            data = self.retry_function(10, urllib2.urlopen, handler)
            picout.write(data.read())
            picout.close()
            os.utime(filename, (int(photo['created']),) * 2)
        except Exception, e:
            self.error(str(e),False)

    def run(self):
        try:
            self.get_albums()
            self.get_pictures()
            self.total = sum(len(album['photos'])
                             for album in self.albums.values())

            # Create Download Directory
            if not os.path.isdir(self.photos_path):
                os.mkdir(self.photos_path)

            for album in self.albums.values():
                self.save_album(album)
        except Exception, e:
            self.exit_if_terminated()
            # print 'DL caught exception', e
            self.error(e)
            self.force_exit() # kill GUI
            sys.exit(1) # kill thread
        self.update(self.index,self.total)