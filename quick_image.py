import os
import firebase_admin
from firebase_admin import credentials, messaging

# 从环境变量读取 JSON 并写入临时文件
json_content = os.environ.get("QUICKIMAGE_JSON")
if not json_content:
    raise ValueError("FIREBASE_JSON secret not set in GitHub Actions")

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

try:
    response = messaging.send(message)
    print('消息发送成功:', response)
except Exception as e:
    print('发送失败:', e)
