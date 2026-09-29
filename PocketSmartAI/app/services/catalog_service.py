from dataclasses import dataclass
@dataclass(frozen=True)
class CatalogEntry:
    id:str; name:str; platform:str; category:str; price:int; description:str; url:str

CATALOG=[
CatalogEntry("home-ikea-lamp","Modern LED Floor Lamp","IKEA","lighting",2499,"Minimal floor lamp for living rooms.","https://www.ikea.com/"),
CatalogEntry("home-amazon-fan","Energy Efficient Ceiling Fan","Amazon","ceiling fan",3299,"Quiet fan suitable for bedrooms and living rooms.","https://www.amazon.in/"),
CatalogEntry("home-amazon-sofa","Compact 3-Seater Sofa","Amazon","sofa",14999,"Space-conscious fabric sofa.","https://www.amazon.in/"),
CatalogEntry("home-ikea-table","4-Seater Dining Table","IKEA","dining table",11990,"Simple dining table for compact homes.","https://www.ikea.com/"),
CatalogEntry("home-flipkart-art","Abstract Wall Art Set","Flipkart","wall art",1899,"Three-piece decorative wall art set.","https://www.flipkart.com/"),
CatalogEntry("home-amazon-rug","Geometric Area Rug","Amazon","rug",2799,"Easy-care rug with a contemporary pattern.","https://www.amazon.in/"),
CatalogEntry("party-zomato-catering","Party Catering Package","Zomato","catering",650,"Illustrative per-person catering allowance.","https://www.zomato.com/"),
CatalogEntry("party-swiggy-catering","Mixed Snacks & Meals Package","Swiggy","catering",550,"Illustrative per-person food allowance.","https://www.swiggy.com/"),
CatalogEntry("party-oyo-room","Guest Accommodation Option","OYO","accommodation",1800,"Illustrative per-room nightly allowance.","https://www.oyorooms.com/"),
CatalogEntry("party-amazon-decor","Birthday Decoration Kit","Amazon","decoration",2499,"Balloons, banner and table decoration kit.","https://www.amazon.in/"),
CatalogEntry("party-flipkart-decor","Elegant Event Decoration Set","Flipkart","decoration",3999,"Reusable event decoration set.","https://www.flipkart.com/"),
CatalogEntry("jewelry-amazon-earrings","Minimal Gold-Tone Earrings","Amazon","earrings",1299,"Versatile earrings for festive and semi-formal outfits.","https://www.amazon.in/"),
CatalogEntry("jewelry-flipkart-necklace","Statement Necklace Set","Flipkart","necklace",2499,"Statement necklace designed for occasion wear.","https://www.flipkart.com/"),
CatalogEntry("jewelry-amazon-bangles","Classic Bangle Set","Amazon","bangles",1799,"Layerable bangle set for traditional styling.","https://www.amazon.in/"),
CatalogEntry("jewelry-flipkart-studs","Pearl Stud Earrings","Flipkart","earrings",999,"Simple pearl-style studs.","https://www.flipkart.com/")]

class CatalogService:
    def search(self,planner,budget,query=""):
        allowed={"home":{"lighting","ceiling fan","sofa","dining table","wall art","rug"},"party":{"catering","accommodation","decoration"},"jewelry":{"earrings","necklace","bangles"}}
        terms={x.lower() for x in query.split() if x}
        items=[x for x in CATALOG if x.category in allowed[planner]]
        if terms:
            scored=[]
            for x in items:
                hay=f"{x.name} {x.category} {x.description} {x.platform}".lower()
                scored.append((sum(t in hay for t in terms),x))
            matched=[x for score,x in sorted(scored,key=lambda z:z[0],reverse=True) if score]
            items=matched or items
        affordable=[x for x in items if x.price<=budget]
        return (affordable or items)[:8]
