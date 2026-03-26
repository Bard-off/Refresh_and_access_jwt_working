from shemas.shemas import UserInfo, TokenInfo, UserIn
from certs import JwtWorking, PwdWorking


john = UserInfo(name="ivan", password=PwdWorking.hash_pdw("1234"), email="ivan@gmail.com", age=20)
sam = UserInfo(name="sam", password=PwdWorking.hash_pdw("qwerty"), email="sam@gmail.com", age=25)

fake_db = {
    john.name: john,
    sam.name: sam
}

