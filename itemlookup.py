import amazonproduct
from amazon_scraper import AmazonScraper
from pandas import DataFrame, read_csv
import pandas as pd
import pdb

f = open('access.txt', 'r')
accesslist = f.readlines()
print accesslist

print len(accesslist[0])
keyid = accesslist[0].strip("\n")
print len(keyid)
accesskey = accesslist[1].strip("\n")
tag = accesslist[2].strip("\n")
amzn = AmazonScraper(keyid,accesskey,tag)
api = amazonproduct.API(locale ='us',access_key_id=keyid,secret_access_key = accesskey,associate_tag = tag)

def price_offers(asin):
    str_asin = str(asin)
    try:
        node = api.item_lookup(ItemId=str_asin, ResponseGroup='Offers', Condition='All', MerchantId='All')        
        for a in node.Items.Item.Offers.Offer:
            price = a.OfferListing.Price.FormattedPrice
            #print a.OfferListing.Price.FormattedPrice
    except Exception:
        print "not found"
        return "NaN"
    #return price
    str_asin = str(asin)

def sales_rank(asin):
    str_asin = str(asin)
    try:
        node = api.item_lookup(ItemId=str_asin, ResponseGroup='SalesRank', Condition='All', MerchantId='All')
        
        for a in node.Items.Item.SalesRank:
            rank = a
            print "rank is", rank
            
            #print a.OfferListing.Price.FormattedPrice
    except Exception:
        print "not found"
        return "NaN"
    #return price
def large_data(asin):
    str_asin = str(asin)
    try:
        node = api.item_lookup(ItemId=str_asin, ResponseGroup='Large', Condition='All', MerchantId='All')
        print node
        print "releasedate is", node.Items.ItemAttributes.ReleaseDate
        for a in node.Items.Item.SalesRank:
            price = a
            print "large data is", price
            
            #print a.OfferListing.Price.FormattedPrice
    except Exception:
        print "not found"
        return "NaN"
    return price    

def main():
    print price_offers("B01637RFR4")
    print price_offers("B00UB76290")
    print large_data("B01637RFR4")
                   
            
if __name__ == "__main__":
    main()
         
       
