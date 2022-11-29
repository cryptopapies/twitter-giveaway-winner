# Twitter Giveaway Winner

Developed by Cryptopapies

[![license-mit](https://img.shields.io/badge/License-MIT-teal.svg)](https://opensource.org/licenses/MIT)
![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

---

## How it works

This Python scripts gets the winner for a giveaway organized on Twitter choosing a random user from the users who satisfy these conditions:

Given a `tweet_id`
the user must have liked the `tweet` and retweeted the `tweet`
AND must follow the provided `username`.

## Get started

1. Install dependencies

    ```pip3 install -r requirements.txt```

2. Setup environment

    Create a `.env` file in the repository root and write this into the file:

    ```txt
    BEARER_TOKEN=YOUR_BEARER_TOKEN_HERE
    ```

3. Run the script

    ```python3 -m twitter_giveaway_winner TWEET_ID YOUR_USERNAME```

## License

twitter-giveaway-winner is licensed under the MIT license.

You can read the entire license [HERE](LICENSE)
