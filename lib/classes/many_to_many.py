
class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise TypeError("Author must be of type Author")
        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be of type Magazine")
        if not isinstance(title, str):
            raise TypeError("Title must be of type str")
        if not (5 <= len(title) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)
        
    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author
    
    @property
    def magazine(self):
        return self._magazine

    @title.setter
    def title(self, value):
        if isinstance(value, str):
            self._title = value
    
    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value
        else:
            raise TypeError("Author must be of type Author")
        
    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
        else:
            raise TypeError("Magazine must be of type Magazine")


class Author:
    def __init__(self, name):
        self._name = None
        self.name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if hasattr(self, '_name') and self._name is not None:
            raise AttributeError("Name cannot be changed after the person is instantiated")
        if not isinstance(value, str):
            raise TypeError("Name must be of type str")
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self._name = value

    def __str__(self):
        return f"Author: {self.name}"
    
    def articles(self):
        return [article for article in Article.all if self == article.author]

    def magazines(self):
        return list({article.magazine for article in self.articles()})
    
    def add_article(self, magazine, title):
        new_article = Article(self, magazine, title)
        self._articles.append(new_article)
        magazine.articles_list.append(new_article) 
        return new_article

    def topic_areas(self):
        topics = {magazine.category for magazine in self.magazines()}
        return list(topics) if topics else None


class Magazine:
    all = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.articles_list = [] 
        Magazine.all.append(self)

    def __str__(self):
        return f"Magazine: {self.name}, Category: {self.category}"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be of type str")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be of type str")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value

    def articles(self):
        return [article for article in Article.all if self == article.magazine]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        article_titles = [article.title for article in self.articles()]
        if article_titles:
            return article_titles
        else:
            return None

    def contributing_authors(self):
        authors = {}
        list_of_authors = []
        for article in self.articles():
            if article.author in authors:
                authors[article.author] += 1
            else:
                authors[article.author] = 1  
        for author in authors:
            if authors[author] >= 2:
                list_of_authors.append(author)   
        if list_of_authors:
            return list_of_authors
        else:
            return None
        
    @classmethod
    def top_publisher(cls):
        publisher_count = {}
        for magazine in cls.all:
            publisher_count[magazine] = len(magazine.articles())
        return max(publisher_count, key=publisher_count.get, default=None)



# Testing Magazine class
print("=== Testing Magazine Class ===")
magazine = Magazine("Title", "Technology")
print(magazine.name) 
magazine.name = "New Title"
magazine.category = "Science"
print(magazine.name)  

# Testing Author class
print("\n=== Testing Author Class ===")
author_1 = Author("Carry Bradshaw")
print(author_1.name)  

# Testing name immutability
try:
    author_1.name = "New Name"  
except AttributeError as e:
    print(e) 

# Testing Article class
print("\n=== Testing Article Class ===")
magazine_1 = Magazine("Vogue", "Fashion")
magazine_2 = Magazine("AD", "Architecture")
article_1 = Article(author_1, magazine_1, "How to wear a tutu with style")
article_2 = Article(author_1, magazine_1, "Dating life in NYC")
article_3 = Article(author_1, magazine_2, "2023 Eccentric Design Trends")
print(article_1.title) 

# Testing article title immutability
try:
    article_1.title = "New Title"  
except AttributeError as e:
    print(e) 

# Testing Object Relationship Methods and Properties
print("\n=== Testing Object Relationships and Properties ===")
print([a.title for a in author_1.articles()])  
print([m.name for m in author_1.magazines()])  
print([a.title for a in magazine_1.articles()]) 
print([str(a) for a in magazine_1.contributors()])  
print(magazine_1.article_titles())  
print([str(a) for a in magazine_1.contributing_authors()]) 

# Testing Aggregate and Association Methods
print("\n=== Testing Aggregate and Association Methods ===")
article_4 = author_1.add_article(magazine_2, "2024 Fashion Trends")
print(article_4.magazine.name) 
print(author_1.topic_areas()) 

# Test Bonus: top_publisher() method
print("\n=== Testing Bonus Method: top_publisher() ===")
print(Magazine.top_publisher())  
