import requests
import time

class YibanSign:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.csrf_token = ""
        self.access_token = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
        }

    def login(self):
        login_url = "https://mobile.yiban.cn/api/v3/passport/login"
        data = {
            "mobile": self.username,
            "password": self.password,
            "imei": ""
        }
        response = self.session.post(login_url, json=data, headers=self.headers)
        if response.status_code == 200 and response.json()["response"] == 100:
            self.csrf_token = response.json()["data"]["csrf_token"]
            self.access_token = response.json()["data"]["user"]["access_token"]
            self.headers["Authorization"] = "Bearer " + self.access_token
            return True
        else:
            return False

    def get_sign_info(self):
        sign_info_url = "https://api.uyiban.com/nightAttendance/student/index/signPosition"
        params = {
            "CSRF": self.csrf_token
        }
        response = self.session.get(sign_info_url, params=params, headers=self.headers)
        if response.status_code == 200 and response.json()["response"] == 100:
            return response.json()["data"]
        else:
            return None

    def sign(self, address, lng, lat):
        sign_url = "https://api.uyiban.com/nightAttendance/student/index/signIn"
        data = {
            "Code": "",
            "PhoneModel": "",
            "SignInfo": {
                "Reason": "",
                "AttachmentFileName": "",
                "LngLat": f"{lng},{lat}",
                "Address": address
            },
            "OutState": "1",
            "CSRF": self.csrf_token
        }
        response = self.session.post(sign_url, json=data, headers=self.headers)
        return response.json()

    def run(self):
        if not self.login():
            print("登录失败")
            return
        
        sign_info = self.get_sign_info()
        if not sign_info:
            print("获取签到信息失败")
            return

        address = sign_info["Address"]
        lng = sign_info["Lng"]
        lat = sign_info["Lat"]

        result = self.sign(address, lng, lat)
        print(result)

if __name__ == "__main__":
    username = "你的易班账号"
    password = "你的易班密码"
    yiban_sign = YibanSign(username, password)
    yiban_sign.run()


