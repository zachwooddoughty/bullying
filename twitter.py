import oauth2
import json

from secrets import *


class Twitter:

    def __init__(self):
        consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        self.client = oauth2.Client(consumer, access_token)

    def search(self, keywords, filter_by="links", limit=5):
        query_string = "+".join('"'+k+"'" for k in keywords) + "+filter:" + filter_by
        search_string = "https://api.twitter.com/1.1/search/tweets.json?q=%s" % query_string
        response, data = self.client.request(search_string)
        data_dict = json.loads(data)

        results = {} 

        if filter_by == 'links':
            for status in data_dict['statuses']:
                try:
                    score = int(status['retweet_count']) + int(status['favorite_count'])
                    urls = status['entities']['urls']
                    for url in urls:
                        link = url['expanded_url']
                        results[link] = max(results.get(link, 0), score)
                except:
                    pass

        elif filter_by == 'images':
            for status in data_dict['statuses']:
                try:
                    score = int(status['retweet_count']) + int(status['favorite_count'])
                    link = status['entities']['media'][0]['media_url']
                    results[link] = max(results.get(link, 0), score)
                except:
                    pass

        return [x[0] for x in sorted(results.items(), key=lambda x: x[1], reverse=True)][:limit]


def main():
    t = Twitter()
    results = t.search(['privacy', 'law', 'google'], filter_by="links")
    print results


if __name__ == "__main__":
    main()
