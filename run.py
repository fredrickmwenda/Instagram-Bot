import time
import os
import configparser

def main():
    from instagrambot import InstagramBot
    #create a config file to pass ur
    #instagram name and password
    confparser = configparser.ConfigParser()
    confparser.read(os.path.expanduser('./check.ini'))

    username = confparser['AUTH']['USERNAME']
    password = confparser['AUTH']['PASSWORD']

    bot = InstagramBot(username,password)
 
    """
    Comment  out the rest when done testing so you can run the check
    Incase you only need to perform a one action only comment out the rest of
    bot actions with  # and leave the action not commented out then run the file
    """
    # bot.clear_notification()
    # bot.like_feed_post(10)
    # bot.comment_image(['Awesome', 'Nice Shot!'])
    # bot.nav_user('teamdreamvillefacts')
    # bot.search_sth('jcole')
    # bot.follow_user('ronaldo')
    # bot.story_by_users(['teamdreamvillefacts', 'martialfc'])
    # bot.story_by_tags(['soccer'])
    # bot.unfollow_user('ronaldo')
    # bot.Like_photoTags_and_comment('neymar','Wow')
    # bot.like_latest_post('martialfc', 10, like=True)
    # bot.comment_post('awesome')
    # bot.stories_all()
    # bot.Likes_photoTags("soccer", 100)




if __name__ == '__main__':
    # running the  script
    main()
