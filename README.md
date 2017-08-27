# worldtemp
Current Sentiment of the World Displayed By Region on a lovely D3.js spinning globe, made for the 2017 UQCS
winter hackathon.

## Dependencies
   - python3
      - tweepy
      - redis
      - flask
      - [vaderSentiment](https://pypi.python.org/pypi/vaderSentiment)
   - redis

---
## Clone and Use or Develop

   1. Clone Repo: `git clone https://github.com/kylelt/worldtemp.git`
   2. [Install redis](https://redis.io/topics/quickstart)
   3. Install Dependencies
   4. Start redis `redis-server`
   5. Start tweet eater `python startstream.py` from `worldtemp/flask_app/twitterscan` directory
   6. Run flask `flask run` from `worldtemp/flask_app directory`
   7. Navigate to http://localhost:5000


