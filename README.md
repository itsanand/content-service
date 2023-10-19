# content-service

## Clone the following repo on your local
```bash
git clone https://github.com/itsanand/user-service.git
git clone https://github.com/itsanand/user-interaction-service.git
git clone https://github.com/itsanand/content-service.git
```

## From user-service folder run the below command 
```bash
docker-compose build
docker-compose up

or

docker-compose up --build
```

### Swagger Docs can be accessed for each service from below urls
```bash
http://localhost:7000/user-interaction-service/docs
http://localhost:8000/user-service/docs
http://localhost:9000/content-service/docs
```

## Content-service Database

```py
class Content:
    """Content model"""

    __tablename__ = "Content"
    title: Column = Column(String, primary_key=True)
    story: Column = Column(String)
    publishedDate: Column = Column(DateTime)
```