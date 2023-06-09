from backend.accessdb import enginer, AccessDB

class Zonemaker:
    def __init__(self, conf):
        self.conf = conf
        self.engine = enginer(self.conf)
    
    def zonecreate(self, zone):
        db = AccessDB(self.engine, self.conf)
        id = db.ZoneCreate(zone)
        if id is False: return False
        return id
    
    def zonepolicy(self, zone_id, data):
        db = AccessDB(self.engine, self.conf)
        state = db.NewZoneRules(zone_id, data)
    
    def zonefilling(self, data):
        db = AccessDB(self.engine, self.conf)
        db.NewDomains(data)
