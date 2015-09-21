import oauth2
import json

from secrets import *


class Twitter:

    def __init__(self):
        consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        self.client = oauth2.Client(consumer, access_token)

    def keyword_search(self, keywords, limit=-1):
        query_string = " OR ".join(keywords) + "&result_type=recent&count=100"
        search_string = "https://api.twitter.com/1.1/search/tweets.json?q=%s" % query_string
        response, data = self.client.request(search_string)
        data_dict = json.loads(data)

        results = {}

        if data_dict.get('statuses') != None:
            for status in data_dict['statuses']:
                mentions = status['entities'].get('user_mentions', [])
                if mentions:
                    text = status['text']
                    for mention in mentions:
                        target = mention['screen_name']

                        bad_name = False
                        for keyword in keywords:
                            if keyword in target:
                                bad_name = True
                        if bad_name:
                            continue
                                
                        mentions = self.mentioned_search(keywords, target) 
                        targets = self.targeted_search(keywords, target)
                        results[target] = list(set(results.get(target, []) + mentions + targets))
        else:
            print "error on keyword search for", query_string, data_dict

        return sorted(results.items(), key=lambda x: len(x[1]), reverse=True)[:limit]

    def mentioned_search(self, keywords, screen_name):
        query_string = " OR ".join(keywords) + " %40" + screen_name + "&result_type=recent&count=100"
        search_string = "https://api.twitter.com/1.1/search/tweets.json?q=%s" % query_string
        response, data = self.client.request(search_string)
        data_dict = json.loads(data)

        results = [] 
        if data_dict.get('statuses') != None:
            for status in data_dict['statuses']:
                results.append(status['text'])
        else:
            print "error on mentioned search for", query_string, data_dict
        return results

    def targeted_search(self, keywords, screen_name):
        query_string = " OR ".join(keywords) + " to:" + screen_name + "&result_type=recent&count=100"
        search_string = "https://api.twitter.com/1.1/search/tweets.json?q=%s" % query_string
        response, data = self.client.request(search_string)
        data_dict = json.loads(data)

        results = [] 
        if data_dict.get('statuses') != None:
            for status in data_dict['statuses']:
                results.append(status['text'])
        else:
            print "error on targeted search for", query_string, data_dict
        return results


def main():
    t = Twitter()
    results = t.keyword_search(["faggot", "fag"])
    for result in results:
        print "===" * 20
        print result[0]
        print "XX"
        print result[1]
        print "===" * 20


if __name__ == "__main__":
    main()
