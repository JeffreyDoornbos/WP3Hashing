from models import Model, APIModel

class OrganizationModel(Model):

    def get_organisaties_count(self):
        query_str = "SELECT COUNT(*) AS count FROM organisaties"
        result = self.query(query_str, first=True)
        print("DEBUG - query result:", dict(result) if result else "None")         
        return result["count"] if result else 0  