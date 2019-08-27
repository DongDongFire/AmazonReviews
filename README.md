# AmazonReviews
Scrpaing Amazon's Customer Reviews

# Description

1. You Only need to get "ASIN" for product page in Amazon(Ex: B06XRKD6B7)

2. Actual Code: you will get dataframe consistings of date, rating, model, title, body.


from DongAmazon import Amazon_dongbot

asin='B06XRKD6B7'
df=Amazon_dongbot.dongbot(asin)
