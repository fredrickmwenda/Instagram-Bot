[InstallationofComponents]
pip install config parser
pip install requests_toolbelt
pip install selenium

[Installsetup]
Download the chromedriver.exe according to your chrome browser
The set chromedriver is for chrome version 80.0.3987.163 otherwise
Download the chromedriver.exe according to your chrome browser 
and set it up in same folder as the bot
You can also set up geckodriver for Firefox browser

<HowTheProjectWorks>
The project has diverse modules divided in sections.

[LoginSection]
Provide your login credentials in the check.ini

[LikeSection] -
- Like user post and comment on their latest post
   bot.like_latest_post('user', 20, like=True)
- Like posts from your own feed[followers/following]
   bot.like_feed_post(60)



[FollowSection]
- Follow users by navigation to their profile pages
   bot.follow_user('user')
- Unfollow a user incase you want to
   bot.unfollow_user('user')

[StoriesSection]
- Watch a specific user story only
   bot.stories_by_user('user')
- Watch a passed list of users stories only
  bot.story_by_users(['user1', 'user2'])
- Watch passed tag set
  bot.story_by_tags(['tag1', 'tag2'])

[CommentSection]
- Comment on a feed image  post using  random comment choices
  bot.comment_image(['Awesome', 'Nice Shot!'])
- Comment on a liked image
   bot.comment_post('awesome')
   

[SearchSection]
- Perform a search on a specific tag
  bot.search_sth('tag')
    


