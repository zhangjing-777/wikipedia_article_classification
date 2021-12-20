import logging
logging.basicConfig(level = logging.DEBUG)
import os
import glob
from wiki_download import WikiDownloader
from config import config
from db import db
logger = logging.getLogger(__name__)



class DownloadTask:

    def download(self):
        for topic in config.keywords:
            logger.info("Download topic {}".format(topic))
            downloader = WikiDownloader(topic)
            downloader.download_articles()

    def save_to_db(self):
        for topic in os.listdir(config.download_path):
            topic_path = os.path.join(config.download_path, topic)
            for article in glob.glob(os.path.join(topic_path,"*.txt")):
                content = open(article, "r").read()
                db.insert(content, topic)

if __name__ == "__main__":
    task = DownloadTask()
    db.drop()
    task.download()
    task.save_to_db()
    
