from memory import get_learned_topics

def filter_new_articles(articles):
    learned = get_learned_topics()
    return [a for a in articles if a["title"] not in learned]
