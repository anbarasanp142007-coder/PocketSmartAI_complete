def login(client):
    u={"email":"demo@example.com","password":"Password123!","full_name":"Demo User"}
    assert client.post("/register",json=u).status_code==201
    assert client.post("/login",json={"email":u["email"],"password":u["password"]}).status_code==200

def test_health(client): assert client.get("/health").json()["status"]=="ok"
def test_auth(client):
    login(client); assert client.get("/session-info").json()["authenticated"] is True
def test_home(client):
    login(client)
    r=client.post("/generate-home",json={"budget":50000,"currency":"INR","style":"modern","rooms":[{"room_type":"Living Room","quantity":1,"items":["sofa","lighting"]}],"priorities":["budget"]})
    assert r.status_code==200 and r.json()["planner"]=="home"
    h=client.get("/history").json(); assert len(h)==1
    assert client.get(f"/recommendations-details/{h[0]['id']}").status_code==200
def test_party(client):
    login(client); r=client.post("/generate-party",json={"budget":75000,"currency":"INR","guest_count":30,"event_type":"Birthday","city":"Chennai","preferences":["vegetarian"]})
    assert r.status_code==200 and r.json()["planner"]=="party"
def test_jewelry(client):
    login(client); r=client.post("/generate-jewelry",data={"budget":"10000","currency":"INR","occasion":"Wedding","style":"elegant","outfit_description":"red saree","color_preferences":"gold,red"})
    assert r.status_code==200 and r.json()["planner"]=="jewelry"
def test_protected(client): assert client.get("/history").status_code==401
