class Article:
    all = []

    def __init__(self, author, magazine, title):
        self._author = self.validate_instance(author, Author, "Author")
        self._magazine = self.validate_instance(magazine, Magazine, "Magazine")
        self.__title = self.validate_string_with_length(title, "Title", 5, 50)
        Article.all.append(self)
        author._articles.append(self)
        magazine._articles.append(self)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, _):
        raise Exception("Title cannot be changed")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = self.validate_instance(value, Author, "Author")

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        self._magazine = self.validate_instance(value, Magazine, "Magazine")

    @staticmethod
    def validate_instance(value, cls, field_name):
        if not isinstance(value, cls):
            raise ValueError(f"{field_name} must be of type {cls.__name__}")
        return value

    @staticmethod
    def validate_string_with_length(value, field_name, min_len, max_len):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        if not (min_len <= len(value) <= max_len):
            raise ValueError(f"{field_name} must be between {min_len} and {max_len} characters")
        return value


class Author:
    def __init__(self, name):
        self.__name = self.validate_non_empty_string(name, "Name")
        self._articles = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, _):
        raise Exception("Author name cannot be changed")

    def add_article(self, magazine, title):
        new_article = Article(self, magazine, title)
        self._articles.append(new_article)
        return new_article

    def articles(self):
        return self._articles

    def magazines(self):
        return list(set([article.magazine for article in self._articles]))

    def topic_areas(self):
        if not self._articles:
            return None
        return list(set([article.magazine.category for article in self._articles]))

    @staticmethod
    def validate_non_empty_string(value, field_name):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError(f"{field_name} must be a non-empty string")
        return value


class Magazine:
    all = []

    def __init__(self, name, category):
        self._name = self.validate_string_with_length(name, "Name", 2, 16)
        self._category = self.validate_non_empty_string(category, "Category")
        self._articles = []
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.validate_string_with_length(value, "Name", 2, 16)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = self.validate_non_empty_string(value, "Category")

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set([article.author for article in self.articles()]))

    def article_titles(self):
        articles = self.articles()
        if not articles:
            return None
        return [article.title for article in articles]

    def contributing_authors(self):
        articles = self.articles()
        if not articles:
            return None
        author_count = {}
        for article in articles:
            author = article.author
            if author in author_count:
                author_count[author] += 1
            else:
                author_count[author] = 1
        return [author for author, count in author_count.items() if count > 2]

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        article_count = {magazine: len(magazine.articles()) for magazine in cls.all}
        return max(article_count, key=article_count.get)

    @staticmethod
    def validate_non_empty_string(value, field_name):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError(f"{field_name} must be a non-empty string")
        return value

    @staticmethod
    def validate_string_with_length(value, field_name, min_len, max_len):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        if not (min_len <= len(value) <= max_len):
            raise ValueError(f"{field_name} must be between {min_len} and {max_len} characters")
        return value
