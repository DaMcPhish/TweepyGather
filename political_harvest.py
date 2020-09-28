#!/usr/local/bin/python
#
#
import csv
import os.path
import tweepy
import twitter_credentials


class Harvester():
    def __init__(self, API_Key=twitter_credentials.API_Key, API_Secret=twitter_credentials.API_Secret,
                 Access_Token=twitter_credentials.Access_Tok,
                 Access_Token_Secret=twitter_credentials.Access_Tok_Secret):
        self.tweepy = tweepy
        self.tweet = []
        auth = tweepy.OAuthHandler(API_Key, API_Secret)
        auth.set_access_token(Access_Token, Access_Token_Secret)
        self.api = tweepy.API(auth)  # API object

    def pol_search(self, in_file):
        # BOUNDBOX_US = [-126.47, 24.39, -63.92, 49.72]
        # twitter_api.trends.place(_id=US_WOE_ID)
        file_exists = os.path.isfile(f'{in_file}.csv')
        with open(f'{in_file}.csv', 'a') as csvFile:
            fields = ['ID', 'Text', 'Time', 'Name', 'Username', 'Location', 'LAT', 'LONG']
            csvGenerate = csv.DictWriter(csvFile, fieldnames=fields)

            if not file_exists:
                csvGenerate.writeheader()
                # max_in = 1000
            # else:
            #     csvFile.close()
            #     exit(1)

            results = self.api.search(q='politics -filter:retweets',
                                      show_user=True,
                                      lang='en',
                                      tweet_mode='extended',
                                      since="2020-09-22",
                                      until="2020-09-28",
                                      country='United States',
                                      count=1000
                                      )
            # if max_in == 0:
            #     csvFile.close()
            #     exit(4)
            # else:
            for tweet in results:
                if tweet.user.location == '' or tweet.user.location == "United States":
                    continue
                else:
                    text = self.strip_non_ascii(tweet.full_text)
                    text.replace('\n', ' ')
                    loc = self.strip_non_ascii(tweet.user.location)
                    usr_name = self.strip_non_ascii(tweet.user.screen_name)
                    name = self.strip_non_ascii(tweet.user.name)
                    lon = "NULL"
                    lat = "NULL"
                    if (tweet.coordinates is not None):
                        lon = tweet.coordinates['coordinates'][0]
                        lat = tweet.coordinates['coordinates'][1]

                    csvGenerate.writerow({'ID': tweet.id_str,
                                          'Text': text,
                                          'Time': tweet.created_at,
                                          'Name': name,
                                          'Username': usr_name,
                                          'Location': loc,
                                          'LAT': lat,
                                          'LONG': lon,
                                          })


# From Jacob Moore https://towardsdatascience.com/@jacob.d.moore1
    def strip_non_ascii(self, string):
        """ Returns the string without non ASCII characters"""
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)


if __name__ == "__main__":
    log_file = 'dat'
    new_search = Harvester()
    new_search.pol_search(log_file)
