from .catalog_service import CatalogService,CatalogEntry
from .gemini_service import GeminiService
from ..schemas import *
class RecommendationService:
    def __init__(self): self.catalog=CatalogService(); self.gemini=GeminiService()
    def item(self,x): return CatalogItem(id=x.id,name=x.name,platform=x.platform,category=x.category,price=x.price,description=x.description,url=x.url)
    def fallback(self,planner,budget,currency,query,title,allocation):
        return RecommendationResponse(
            planner=planner,title=title,budget=budget,currency=currency,budget_allocation=allocation,
            recommendations=[Recommendation(item=self.item(x),reason="Selected from the built-in demo catalog as a budget-conscious option.",estimated_total=x.price) for x in self.catalog.search(planner,budget,query)],
            tips=["Catalog prices are illustrative until connected to a live provider.","Compare delivery, taxes, installation and service fees.","Keep a contingency reserve instead of allocating the entire budget."],
            disclaimer="Demo catalog data is illustrative and is not live inventory or a price quote."
        )
    def prompt(self,planner,payload,catalog):
        cat="\n".join(f"- id={x.id}; name={x.name}; platform={x.platform}; category={x.category}; price={x.price} INR; url={x.url}; description={x.description}" for x in catalog)
        return f"""Create a {planner} budget plan.
USER INPUT:
{payload}
AVAILABLE CATALOG:
{cat}
Rules: stay within budget; use only catalog IDs; preserve catalog metadata exactly; provide 3-8 useful recommendations; explain choices; never claim live marketplace checks."""
    def generate_home(self,r):
        q=" ".join([r.style,*r.priorities,*(i for room in r.rooms for i in room.items)])
        cat=self.catalog.search("home",r.budget,q)
        alloc={"furniture":int(r.budget*.45),"lighting_decor":int(r.budget*.30),"contingency":int(r.budget*.25)}
        try:
            if self.gemini.enabled:return self.gemini.generate(self.prompt("home interior",r.model_dump(),cat))
        except Exception: pass
        return self.fallback("home",r.budget,r.currency,q,"Home Interior Budget Plan",alloc)
    def generate_party(self,r):
        q=f"{r.event_type} {r.city or ''} {' '.join(r.preferences)}"
        cat=self.catalog.search("party",r.budget,q)
        alloc={"food":int(r.budget*.45),"decoration":int(r.budget*.20),"venue_accommodation":int(r.budget*.20),"contingency":int(r.budget*.15)}
        try:
            if self.gemini.enabled:return self.gemini.generate(self.prompt("party",r.model_dump(),cat))
        except Exception: pass
        return self.fallback("party",r.budget,r.currency,q,"Party Budget Plan",alloc)
    def generate_jewelry(self,r,image_bytes=None,image_mime=None):
        q=f"{r.occasion} {r.style} {' '.join(r.color_preferences)} {r.outfit_description or ''}"
        cat=self.catalog.search("jewelry",r.budget,q)
        alloc={"primary_jewelry":int(r.budget*.70),"accessories":int(r.budget*.15),"contingency":int(r.budget*.15)}
        try:
            if self.gemini.enabled:return self.gemini.generate(self.prompt("jewelry",r.model_dump(),cat),image_bytes,image_mime)
        except Exception: pass
        return self.fallback("jewelry",r.budget,r.currency,q,"Jewelry Budget Plan",alloc)
