import requests
from random import randint, choice
import queue
from threading import Thread
from os import system

named            = ["an", "ba", "bach", "bao", "binh", "cao", "chieu", "dai", "dang", "dinh", "duc", "duy", "gia", "hai", "ha", "hoai", "hoang", "huu", "khac", "khai", "khoi", "kiet", "ky", "lac", "lam", "lap", "manh", "minh", "nghia", "nghi", "nguyen", "nhat", "phi", "phong", "phu", "phuc", "phuoc", "phuong", "quang", "quoc", "quy", "song", "sy", "tam", "tan", "thai", "thanh", "the", "thien", "thieu", "thinh", "thoi", "thong", "thuan", "thuong", "thuy", "tien", "tieu", "ton", "tri", "trieu", "trong", "truong", "tuong", "van", "viet", "vu", "vinh", "xuan", "chi", "cong", "cuong", "danh", "dat", "dung", "duong", "hoa", "hoan", "hong", "huy", "kien", "ngoc", "toan", "trung", "tu", "tung", "anh", "bang", "buu", "cat", "chan", "che", "chien", "chung", "dac", "dan", "dong", "hao", "hien", "hieu", "ho", "hung", "khang", "phung", "son", "thach", "tuan", "hiep", "mong", "niem", "kim", "chuan", "hanh", "chau", "chinh", "giang", "vien", "quyet", "chuong", "doan", "huan", "khanh", "nhan", "nhu", "ta", "that", "tai", "thang", "truc", "tuyen", "uy", "nam", "tich", "ly", "thu", "lien", "huong", "luong", "vuong", "khuong", "dien", "thdienh", "doanh", "hau", "huynh", "kha", "khiem", "khoa", "linh", "loc", "loi", "long", "luan", "nhut", "lo", "phat", "vy", "lai", "quan", "chanh", "sang", "thiet", "em", "anh", "tho", "tin", "triet", "liem", "mai", "trinh", "man", "vi", "ca", "cam", "cuc", "dao", "dieu", "diu", "giao", "han", "hang", "hue", "", "kieu", "lan", "lieu", "loan", "nga", "ngan", "nguyet", "nha", "nhi", "nhung", "oanh", "quyen", "quynh", "san", "thao", "tra", "tram", "tran", "trang", "huyen", "le", "my", "suong", "uyen", "tham", "tuyet", "yen", "ai", "di", "diem", "duyen", "khue", "su", "khe", "nhien", "que", "thi", "thoa", "thuc", "khuyen", "mien", "thuy", "bich"]

class Register:
    def __init__(self, thread) -> None:
        self.thread = thread
        self.base_url = "https://trangnguyen.edu.vn/dang-ky"
        self.queue_write = queue.Queue()
        self.queue_decrease = queue.Queue()
        self.running = True

    def get_name(self):
        global named

        new_name = ""
        random_name          = [choice(named) for i in range(randint(2,3))] + [str(randint(1,10000))]
        random_postition = randint(1, len(random_name) - 1)
        v = []
        for i in range(random_postition):
            new_name += random_name[i]
            v.append(random_name[i])
        for i in v:
            random_name.pop(random_name.index(i))
        return new_name + "".join(random_name)

    def _headers(self):
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://trangnguyen.edu.vn',
            'priority': 'u=1, i',
            'referer': 'https://trangnguyen.edu.vn/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }

    def register(self, id):
        json_data = {
            'fullname': 'Lê Minh Trí',
            'username': self.get_name(),
            'password': 'Trangnguyenedu24',
            'schoolGrade': 1,
            'gender': 'MALE',
            'provinceId': '8b16d771-72f4-426b-b4f0-3e606f4ac3f4',
            'districtId': 'c34a30b9-7941-4c6f-9a3e-61767ff75d7b',
            'schoolId': 'dac89e13-7fc4-4d1c-a51c-0bb9e0ff288c',
            'schoolClassId': '0caa6b2c-86e4-4753-a62c-0848dfb61185',
            'agree': 'on',
        }

        response = requests.post(
            url     = 'https://api-v5.trangnguyen.edu.vn/v5/users/register', 
            headers = self._headers(), 
            json    = json_data
        )
        if response.status_code == 200:
            try:
                print(f'thread {id}: userNumber: {response.json()["data"]["user"]["userNumber"]}')
                self.queue_write.put(f"Tài khoản: {json_data['username']} , Mật khẩu : Trangnguyenedu24\n")
                self.queue_decrease.put("1")
            except:
                print(response.json())
        else:
            print(f"thread {id}: Failed to register")

    def show(self):
        while self.running:
            system(f"title Process left {self.thread}")

    def queue_writes(self):
        while self.running:
            try:
                log = self.queue_write.get_nowait()
                with open("account.txt", "a", encoding="utf-8") as f:
                    f.write(log)
            except queue.Empty:
                continue
            
    def queue_decreases(self):
        while self.running:
            try:
                log = self.queue_decrease.get_nowait()
                if log == "1":
                    self.thread -= 1
            except queue.Empty:
                continue

    def multithreading(self):
        Thread(target=self.queue_decreases).start()
        Thread(target=self.show).start()
        Thread(target=self.queue_writes).start()
        while self.thread > 0:
            t = []
            
            for i in range(self.thread):
                t.append(Thread(target=self.register, args = (i,)))
            for i in t:
                i.start()
            for i in t:
                i.join()
        self.running = False

Register(int(input("enter total account you want to register: "))).multithreading()
input("--Press any key to exit--")