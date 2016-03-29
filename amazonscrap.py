import amazonproduct
from amazon_scraper import AmazonScraper
from pandas import DataFrame, read_csv
import pandas as pd
import pdb

amzn = AmazonScraper("AKIAJN3L3SMT3S7K4MBQ", "Qv1QZLJJw3kKr7K4HqKycd285LoxwcGwBrptoC9/", "amazonscrap-20")
api = amazonproduct.API(locale ='us',access_key_id= "AKIAJN3L3SMT3S7K4MBQ",secret_access_key = "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",associate_tag = "amazonscrap-20")

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
    return price
def main():
    print price_offers("B0017JHVNW")
    items = api.item_search('Software', Sort = "salesrank", ItemPage = 1 ,Keywords = " ")
    print len(items)
    p = " "
    i = 0
    #Getting product id of any software product to reach ids of software node in general
    for product in items:
        print product.ASIN
        i = i + 1 
        p = str(product.ASIN)  
        print 's: "%s"' % (product.ItemAttributes.Title)
        break;

    print "No reterived", i

    #Finding the root name of the category the product belongs to
    result = api.item_lookup(p,ResponseGroup='BrowseNodes')
    root_ids = result.xpath('//aws:BrowseNode[aws:IsCategoryRoot=1]/aws:BrowseNodeId',namespaces={'aws': result.nsmap.get(None)})
    print api.browse_node_lookup(root_ids[0]).BrowseNodes.BrowseNode.Ancestors.BrowseNode.Name 

    #software nodes browser id
    softwareId = api.browse_node_lookup(root_ids[0]).BrowseNodes.BrowseNode.Ancestors.BrowseNode.BrowseNodeId
    print softwareId


    # TopSellers for in software can't get above 10
    result = api.browse_node_lookup(softwareId, 'TopSellers')
    print result.BrowseNodes.BrowseNode.TopSellers.countchildren
    for item in result.BrowseNodes.BrowseNode.TopSellers.TopSeller:
        print item.ASIN.text, item.Title.text
        #rs = amzn.reviews(ItemId=item.ASIN)
        #r = amzn.review(Id=rs.ids[0])
        #print len(rs.ids) #10
        #print r.text

    #get top products from all cateogries in software
    index = 0
    pindex = []
    pidList = []
    pTitleList = []
    catList = []
    priceList = []
    result = api.browse_node_lookup(root_ids[0])
    for child in result.BrowseNodes.BrowseNode.Children.BrowseNode:
         print '(%s %s)' % (child.Name, child.BrowseNodeId)
         bId = child.BrowseNodeId       
         catname = child.Name.text         
         #getresults(child.BrowseNodeId.text,child.Name)
         items = api.item_search('Software', Sort = "salesrank", ItemPage = 1 ,BrowseNode = bId)
         for product in items:
             print product.ASIN.text.encode('utf-8')
             print product.ItemAttributes.Title.text.encode('utf-8')
             index = index + 1
             pindex.append(index)
             pidList.append(product.ASIN.text.encode('utf-8'))
             pTitleList.append(product.ItemAttributes.Title.text.encode('utf-8'))
             catList.append(catname.encode('utf-8'))            
             priceList.append(price_offers(product.ASIN.text))
        
    ProductDataSet = list(zip(pindex,pidList,pTitleList,catList,priceList))
    df = pd.DataFrame(data = ProductDataSet, columns=['Index', 'ProductID','ProductTitle','Category','Price'])
    print df
    df.to_csv('productdataset.csv',index=False,header=True)
    
                   
            
if __name__ == "__main__":
    main()
         
       
