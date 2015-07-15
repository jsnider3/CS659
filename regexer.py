import re

##
class Product(object):

  def __init__(self, title):
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

  def num_reviews(self):
    return len(self.reviews)


##
class Review(object):
  
  def __init__(self, time, text):
    self.time = time
    self.text = text

##

def products_by_conciseness(prods):
  vals = prods.values()
  vals.sort(key=lambda k: k.conciseness())
  return vals

def products_by_num_reviews(prods):
  vals = prods.values()
  vals.sort(key=lambda k: k.num_reviews())
  return vals

def main():
  products = dict()
  with open('Kindle_Store.txt') as f:
    data = ''.join(f.readlines())
    field = '.*?/.*?: .*?\n'
    getfield = '.*?/.*?: (.*?)\n'
    productId = 'product/productId: (.*?)\n'
    productTitle = 'product/title: (.*?)\n'
    reviewtime = 'review/time: (.*?)\n'
    reviewtext = 'review/text: (.*?)\n'
    review = (field + productTitle + field * 5 +
      reviewtime + field + reviewtext + '\n')
    for match in re.finditer(review, data):
      title = match.group(1)
      prod_review = Review(match.group(2),match.group(3))
      if title not in products:
        products[title] = Product(title)
      products[title].add_review(prod_review)
    vals = reversed(products_by_conciseness(products))
    for p in vals:#products.values():
      print(p, p.conciseness())

if __name__ == "__main__":
  main()
