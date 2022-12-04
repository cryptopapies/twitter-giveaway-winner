from dotenv import load_dotenv
from sys import argv, exit
import tweepy
from typing import List, Optional
from random import choice
from os import getenv


load_dotenv()


class Client(object):
    def __init__(self, bearer_token: str) -> None:
        self.__client = tweepy.Client(bearer_token)

    def likes(self, tweet: str) -> List[str]:
        """Get list of user who liked this tweet"""
        return self.__get_likes([], tweet, None)

    def retweets(self, tweet: str) -> List[str]:
        """Get list of user who retweeted this tweet"""
        return self.__get_retweets([], tweet, None)

    def followers(self, username: str) -> List[str]:
        """Get list of username who follows `username`"""
        # get_users_followers(user_id)
        user = self.__client.get_user(id=None, username=username)
        if user:
            return self.__get_followers([], user.data["id"], None)
        else:
            raise Exception(f"{username} not found")

    def __get_likes(
        self, users: List[str], tweet: str, token: Optional[str]
    ) -> List[str]:
        data = self.__client.get_liking_users(tweet, pagination_token=token)
        meta = data.meta
        # base case
        if meta["result_count"] == 0:
            return users
        users.extend(map(lambda x: x["username"], data.data))
        return self.__get_likes(users, tweet, meta["next_token"])

    def __get_retweets(
        self, users: List[str], tweet: str, token: Optional[str]
    ) -> List[str]:
        data = self.__client.get_retweeters(tweet, pagination_token=token)
        meta = data.meta
        # base case
        if meta["result_count"] == 0:
            return users
        users.extend(map(lambda x: x["username"], data.data))
        return self.__get_likes(users, tweet, meta["next_token"])

    def __get_followers(
        self, users: List[str], user_id: str, token: Optional[str]
    ) -> List[str]:
        data = self.__client.get_users_followers(
            user_id, max_results=1000, pagination_token=token
        )
        meta = data.meta
        # base case
        if meta["result_count"] == 0:
            return users
        new_users: List[str] = list(map(lambda x: x["username"], data.data))
        next_token = None
        if meta.get("next_token"):
            next_token = meta["next_token"]
        else:
            users.extend(new_users)
            return users
        users.extend(new_users)
        return self.__get_followers(users, user_id, next_token)


def filter_eligible_winners(
    liked: List[str], retweets: List[str], followers: List[str]
) -> List[str]:
    """Get eligible winner usernames"""
    eligibles: List[str] = list(filter(lambda x: x in retweets, liked))
    eligibles: List[str] = list(filter(lambda x: x in followers, eligibles))
    return eligibles


def main(args: List[str]) -> int:
    if len(args) < 2:
        print("Usage: twitter-giveaway-winner <tweet_id> <account_name>")
        return 255

    tweet_id = args[0]
    account_name = args[1]
    client = Client(getenv("BEARER_TOKEN"))
    liking_users = client.likes(tweet_id)
    retweeting_users = client.retweets(tweet_id)
    followers = client.followers(account_name)

    eligible_winners = filter_eligible_winners(
        liking_users, retweeting_users, followers
    )
    if len(eligible_winners) == 0:
        print("No eligible winner found")
        return 1

    print("eligible winners:")
    for eligible in eligible_winners:
        print(f"@{eligible}")
    winner = choice(eligible_winners)
    print(f"The winner is: {winner}")

    return 0


if __name__ == "__main__":
    exit(main(argv[1:]))
