import os
import firebase_admin
from firebase_admin import credentials, messaging

# 从环境变量读取 JSON 并写入临时文件
json_content = os.environ.get("QUICKIMAGE_JSON")
if not json_content:
    raise ValueError("QUICKIMAGE_JSON secret not set in GitHub Actions")

with open("firebase.json", "w") as f:
    f.write(json_content)

# 初始化 Firebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

# 构建消息
message = messaging.Message(
    data={
        "type": "wakeup1",
        "content": "唤醒应用1"
    },
    android=messaging.AndroidConfig(
        priority='high'
    ),
    topic="all_users"
)
# ✅ 计数文件
COUNT_FILE = "send_count.txt"

def get_send_count():
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_send_count(count):
    with open(COUNT_FILE, "w") as f:
        f.write(str(count))

# ✅ 发送消息
try:
    response = messaging.send(message)
    print("消息发送成功:", response)

    # 更新发送次数
    count = get_send_count() + 1
    save_send_count(count)
    print(f"累计发送次数: {count}")

except Exception as e:
    print("发送失败:", e)
