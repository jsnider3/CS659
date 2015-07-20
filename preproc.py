#!/usr/bin/env python2
''' Preprocess the Amazon reviews and output them
    in a way that Weka can process.
    @author: Josh Snider.'''
import datetime
import re

##
class Product(object):
  ''' An Amazon product with a title and a list of reviews.'''

  def __init__(self, title):
    ''' Product wih no reviews.'''
    self.title = title
    self.reviews = []

  def __repr__(self):
    return str(self)

  def __str__(self):
    return self.title + " with " + str(self.num_reviews()) + " reviews."

  def add_review(self, review):
    self.reviews.append(review)

  def conciseness(self):
    wc = [len(r.text.split(' ')) for r in self.reviews]
    return sum(wc) / len(wc)

  def filter_reviews(self, filt):
    self.reviews = [review for review in self.reviews if filt(review)]

  def num_reviews(self):
    return len(self.reviews)

##
class Review(object):
  
  def __init__(self, time, text):
    self.time = datetime.datetime.fromtimestamp(float(time))
    self.text = text

##

def filter_products(prods, filt):
  ''' Filter the reviews with filt and remove
      products with no reviews.'''
  for key in prods.keys():
    prods[key].filter_reviews(filt)
    if not prods[key].num_reviews():
      del prods[key]

def products_by_conciseness(prods):
  vals = prods.values()
  vals.sort(key=lambda k: k.conciseness())
  return vals

def products_by_num_reviews(prods):
  vals = prods.values()
  vals.sort(key=lambda k: k.num_reviews())
  return vals

JAN01_1970 = datetime.datetime.fromtimestamp(0.0)
JAN01_2011 = datetime.datetime.fromtimestamp(1293840000.0)
JAN01_2020 = datetime.datetime.fromtimestamp(1577836800.0)
def timestamp_filter(start=JAN01_1970, stop=JAN01_2020):
  return lambda review: start < review.time < stop

def get_reviews(data):
  field = '.*?/.*?: .*?\n'
  getfield = '.*?/.*?: (.*?)\n'
  productId = 'product/productId: (.*?)\n'
  productTitle = 'product/title: (.*?)\n'
  reviewtime = 'review/time: (.*?)\n'
  reviewtext = 'review/text: (.*?)\n'
  review = (field + productTitle + field * 5 +
    reviewtime + field + reviewtext + '\n')
  for match in re.finditer(review, data):
    yield match

def filter_products_by_reviews(prods, cutoff):
  ''' Remove the products with less than
      cutoff reviews..'''
  for key in prods.keys():
    if prods[key].num_reviews() < cutoff:
      del prods[key]

def filter_products_by_title(prods, whitelist):
  ''' Remove the products with less than
      cutoff reviews..'''
  for key in prods.keys():
    if key not in whitelist:
      del prods[key]

def main():
  products = dict()
  with open('Kindle_Store.txt') as f:
    data = ''.join(f.readlines())
    for match in get_reviews(data):
      title = match.group(1)
      prod_review = Review(match.group(2), match.group(3))
      if title not in products:
        products[title] = Product(title)
      products[title].add_review(prod_review)
    filter_products(products,timestamp_filter(start=JAN01_2011))
    filter_products_by_reviews(products, 200)
    vals = (products_by_num_reviews(products))
    for p in vals:
      print(p)

if __name__ == "__main__":
  main()
