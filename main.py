#!/usr/bin/env python3
import falcon.asgi as falcon
from pymongo import MongoClient
import logging

from resources import BookResource, BooksResource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    async def process_request(self, req, resp):
        logger.info(f"Request: {req.method} {req.uri}")

    async def process_response(self, req, resp, resource, req_succeeded):
        logger.info(f"Response: {resp.status} for {req.method} {req.uri}")


# Initialize MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')
db = client.bookstore

# Create the Falcon application
app = falcon.App(middleware=[LoggingMiddleware()])

# Instantiate the resources
book_resource = BookResource(db)
books_resource = BooksResource(db)

# Add routes to serve the resources
app.add_route('/books', books_resource)
app.add_route('/books/{book_id}', book_resource)