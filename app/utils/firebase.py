# Firebase初期化と設定
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# Firebase初期化（シングルトンパターン）
_db = None

def get_firestore_db():
    """Firestoreデータベースインスタンスを取得"""
    global _db
    
    if _db is None:
        # Firebase Admin SDKの初期化
        if not firebase_admin._apps:
            # 環境変数から認証情報を取得
            project_id = os.getenv("FIREBASE_PROJECT_ID")
            private_key = os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n")
            client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
            
            if project_id and private_key and client_email:
                # サービスアカウントキーから認証情報を作成
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": project_id,
                    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID", ""),
                    "private_key": private_key,
                    "client_email": client_email,
                    "client_id": os.getenv("FIREBASE_CLIENT_ID", ""),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL", ""),
                })
                firebase_admin.initialize_app(cred)
            else:
                # デモモード（Firebase未設定時）
                print("警告: Firebase設定が不完全です。デモモードで動作します。")
                # デモ用のダミー初期化（実際のFirestoreは使用できない）
                firebase_admin.initialize_app()
        
        _db = firestore.client()
    
    return _db

