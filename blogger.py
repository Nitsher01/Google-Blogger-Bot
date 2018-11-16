from get_events import get_daily_events
import datetime
import sys
from oauth2client import client
from googleapiclient import sample_tools


def main(argv):
  # Authenticate and construct service.
  print('Starting at ', datetime.date.today())
  events = get_daily_events()

  service, flags = sample_tools.init(
      argv, 'blogger', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/blogger')

  try:
      print('These event found ', len(events))
      users = service.users()

      # Retrieve this user's profile information
      thisuser = users.get(userId='self').execute()
      print('This user\'s display name is: %s' % thisuser['displayName'])

      blogs = service.blogs()

      # Retrieve the list of Blogs this user has write privileges on
      thisusersblogs = blogs.listByUser(userId='self').execute()
      for blog in thisusersblogs['items']:
        print('The blog named \'%s\' is at: %s' % (blog['name'], blog['url']))

      posts = service.posts()
      today = datetime.date.today()
      # List the posts for each blog this user has
      title = 'On ' + today.strftime('%d %B') + ' in History'
      sorted_keys = sorted(events)
      contentList = []
      post_count = 0
      #Creating ad :P
      ads = '''<script type="text/javascript" language="javascript">
      var aax_size='728x90';
      var aax_pubname = 'astr0c-21';
      var aax_src='302';
    </script>
    <script type="text/javascript" language="javascript" src="https://c.amazon-adsystem.com/aax2/assoc.js"></script>
      '''
      for keys in sorted_keys:
        tmp_ls = events[keys].split()
        post_count += 1
        # Creating the div for individual result
        div_str = ('''<div style = "-webkit-border-radius: 10px 10px 10px 10px;
        border-radius: 10px 10px 10px 10px;
        margin: 10px;
        background-color: #FAFAFA;padding: 20px;"><p>''') + ('<b>') + (' '.join(tmp_ls[0:2])) + ('</b> ') + (' '.join(tmp_ls[2:6])) +(' <b><u>') + (tmp_ls[6]) + ('</b></u> ') + (' '.join(tmp_ls[7:])) + ('</p></div>')
        contentList.append(div_str)
        if post_count % 10 == 0:
          contentList.append(ads)
      content = "".join(contentList) + '<br><p>Download <b>On This Day in History</b> app for your android device from <a href = "https://play.google.com/store/apps/details?id=com.what.does.date.says">Play Store</a></p></br>'
      #print(content)
      #enter blogId of the blog you want to post
      nw_post = posts.insert(blogId = '6411519884266121347',body = {
              "title": title, # The title of the Post.
              "content" : content
            }).execute()
      print('This happened while trying to create post ', nw_post['url'])
      for blog in thisusersblogs['items']:
        print('The posts for %s:' % blog['name'])
        request = posts.list(blogId=blog['id'])
        while request != None:
          posts_doc = request.execute()
          if 'items' in posts_doc and not (posts_doc['items'] is None):
            for post in posts_doc['items']:
              print('  %s (%s)' % (post['title'], post['url']))
          request = posts.list_next(request, posts_doc)

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
