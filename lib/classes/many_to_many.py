from collections import Counter

class Article:
    all = []
    
    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        self._title = title

        self.author = author
        self.magazine = magazine
        Article.all.append(self)

    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("Author must be of type Author")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    
    
    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError("Magazine must be of type Magazine")
        self._magazine = value

class Author:
    def __init__(self, name):
        if not isinstance(name,str):
            raise TypeError("Name must be of type str")
        if len(name) == 0:
            raise ValueError('Name must be longer than 0 characters')
        self._name = name

    @property
    def name(self):
        return self._name
    
    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list(set(article.magazine for article in self.articles()))
        
    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be of type Magazine.")
        return Article(self, magazine, title)
        
    def topic_areas(self):
        magazine_categories = [article.magazine.category for article in self.articles()]
        if magazine_categories:
            return list(set(magazine_categories))
        return None

class Magazine:
    magazines = []
    def __init__(self, name, category):
        self.name = name
        self._category = category
        Magazine.magazines.append(self)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value,str) and (2 <= len(value) <=16):
            self._name = value
        else:
            raise ValueError('Name must be of type string and between 2 and 16 characters')
        
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError('Category must be of type string and have length greater than 0')
        self._category = value

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        if titles:
            return titles
        return None

    def contributing_authors(self):
        authors = Counter(article.author for article in self.articles())
        result = [author for author, count in authors.items() if count > 2]
        return result if result else None
    
    @classmethod
    def top_publisher(cls):
        if not cls.magazines:
            return None
        top_magazine = max(cls.magazines, key=lambda mag: len(mag.articles()))
        return top_magazine if top_magazine.articles() else None

    
        