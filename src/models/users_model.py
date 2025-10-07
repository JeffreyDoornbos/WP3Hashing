from models import Model, APIModel

class UserModel(Model):

    def __init__(self):
        super().__init__()
        self.__api = APIModel()

    def get_user(self, user_id:int):
        query_str = "SELECT * FROM ervaringsdeskundigen WHERE id=?"
        result = self.query(query_str, user_id, first=True)
        return dict(result) if result else None
    
    def update_user(self, user_id:int, data:dict):
        self.__api.patch_ervaringsdeskundige(user_id, data)

    def create_user(self, data:dict):
        return self.__api.post_ervaringsdeskundige(data)

    def get_user_by_email(self, email:str):
        query_str = "SELECT * FROM ervaringsdeskundigen WHERE email=?"
        result = self.query(query_str, email, first=True)
        return dict(result) if result else None