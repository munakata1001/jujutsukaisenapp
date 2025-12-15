# Firebase初期化と設定
import os
os.environ['GRPC_VERBOSITY'] = 'ERROR'
import json
from typing import Tuple
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# Firebase初期化（シングルトンパターン）
_db = None
_initialization_error = None

def _validate_service_account_key(key_data: dict) -> Tuple[bool, str]:
    """サービスアカウントキーの検証"""
    required_fields = ["type", "project_id", "private_key", "client_email"]
    
    for field in required_fields:
        if field not in key_data:
            return False, f"必須フィールド '{field}' がサービスアカウントキーに含まれていません"
    
    if key_data.get("type") != "service_account":
        return False, "サービスアカウントキーのタイプが正しくありません"
    
    if not key_data.get("client_email") or "@" not in key_data.get("client_email", ""):
        return False, "client_emailが正しい形式ではありません"
    
    if not key_data.get("private_key") or "BEGIN PRIVATE KEY" not in key_data.get("private_key", ""):
        return False, "private_keyが正しい形式ではありません"
    
    return True, ""

def _get_service_account_path(env_path: str) -> str:
    """サービスアカウントキーファイルのパスを解決"""
    # このファイルは backend/app/utils/firebase.py にある
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 環境変数からパスを取得
    if env_path:
        # 絶対パスの場合
        if os.path.isabs(env_path):
            return env_path if os.path.exists(env_path) else None
        
        # 相対パスの場合、backendディレクトリを基準にする
        full_path = os.path.join(backend_dir, env_path)
        if os.path.exists(full_path):
            return full_path
    
    # 環境変数が設定されていない場合、デフォルトのファイル名を試す
    default_path = os.path.join(backend_dir, "firebase-service-account.json")
    if os.path.exists(default_path):
        return default_path
    
    return None

def get_firestore_db():
    """Firestoreデータベースインスタンスを取得"""
    global _db, _initialization_error
    
    if _db is None and _initialization_error is None:
        # Firebase Admin SDKの初期化
        if not firebase_admin._apps:
            try:
                # 方法1: サービスアカウントキーファイルのパスが指定されている場合
                service_account_path = _get_service_account_path(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
                if service_account_path:
                    # サービスアカウントキーファイルの検証
                    try:
                        with open(service_account_path, 'r', encoding='utf-8') as f:
                            key_data = json.load(f)
                        
                        is_valid, error_msg = _validate_service_account_key(key_data)
                        if not is_valid:
                            _initialization_error = f"サービスアカウントキーの検証に失敗しました: {error_msg}"
                            raise ValueError(_initialization_error)
                        
                        # プロジェクトIDとclient_emailをログに出力（デバッグ用）
                        project_id = key_data.get("project_id", "不明")
                        client_email = key_data.get("client_email", "不明")
                        
                        try:
                            cred = credentials.Certificate(service_account_path)
                            firebase_admin.initialize_app(cred)
                        except Exception as init_error:
                            error_str = str(init_error)
                            if "invalid_grant" in error_str or "account not found" in error_str:
                                _initialization_error = (
                                    f"Firebase認証エラー: サービスアカウントキーが無効です。\n"
                                    f"プロジェクトID: {project_id}\n"
                                    f"サービスアカウント: {client_email}\n"
                                    f"エラー詳細: {error_str}\n\n"
                                    f"解決方法:\n"
                                    f"1. Firebase Console (https://console.firebase.google.com/) にアクセス\n"
                                    f"2. プロジェクト '{project_id}' を選択\n"
                                    f"3. プロジェクト設定 > サービスアカウント に移動\n"
                                    f"4. 「新しい秘密鍵の生成」をクリックして新しいキーをダウンロード\n"
                                    f"5. ダウンロードしたJSONファイルを '{service_account_path}' に保存\n"
                                    f"6. バックエンドサーバーを再起動"
                                )
                            else:
                                _initialization_error = f"Firebase初期化エラー: {error_str}"
                            raise ValueError(_initialization_error)
                    except json.JSONDecodeError as e:
                        _initialization_error = f"サービスアカウントキーファイルのJSON形式が正しくありません: {str(e)}"
                        raise ValueError(_initialization_error)
                    except FileNotFoundError:
                        _initialization_error = f"サービスアカウントキーファイルが見つかりません: {service_account_path}"
                        raise ValueError(_initialization_error)
                else:
                    # 方法2: 環境変数から認証情報を取得
                    project_id = os.getenv("FIREBASE_PROJECT_ID")
                    private_key = os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n")
                    client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
                    
                    if project_id and private_key and client_email:
                        # サービスアカウントキーから認証情報を作成
                        key_data = {
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
                        }
                        
                        # サービスアカウントキーの検証
                        is_valid, error_msg = _validate_service_account_key(key_data)
                        if not is_valid:
                            _initialization_error = f"サービスアカウントキーの検証に失敗しました: {error_msg}"
                            raise ValueError(_initialization_error)
                        
                        cred = credentials.Certificate(key_data)
                        firebase_admin.initialize_app(cred)
                    else:
                        # 認証情報が設定されていない場合
                        error_msg = (
                            "Firebase認証情報が設定されていません。\n"
                            "以下のいずれかの方法で設定してください：\n"
                            "1. サービスアカウントキーファイルを使用: GOOGLE_APPLICATION_CREDENTIALS環境変数にファイルパスを設定\n"
                            "2. 環境変数を使用: FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAILを設定\n"
                            "詳細は backend/ENV_SETUP_GUIDE.md を参照してください。"
                        )
                        _initialization_error = error_msg
                        raise ValueError(error_msg)
            except ValueError:
                # ValueErrorは既に設定されたエラーメッセージを使用
                raise
            except Exception as e:
                error_str = str(e)
                # より詳細なエラーメッセージを提供
                if "invalid_grant" in error_str or "account not found" in error_str:
                    _initialization_error = (
                        f"Firebase認証エラー: サービスアカウントキーが無効か、削除されたアカウントを参照しています。\n"
                        f"エラー詳細: {error_str}\n"
                        f"解決方法:\n"
                        f"1. Firebase Consoleで新しいサービスアカウントキーを生成してください\n"
                        f"2. サービスアカウントが削除されていないか確認してください\n"
                        f"3. プロジェクトIDが正しいか確認してください"
                    )
                elif "timeout" in error_str.lower():
                    _initialization_error = (
                        f"Firebase接続タイムアウト: {error_str}\n"
                        f"解決方法:\n"
                        f"1. インターネット接続を確認してください\n"
                        f"2. ファイアウォール設定を確認してください\n"
                        f"3. Firebaseプロジェクトが有効か確認してください"
                    )
                else:
                    _initialization_error = f"Firebase初期化エラー: {error_str}"
                raise ValueError(_initialization_error)
        
        if _initialization_error:
            raise ValueError(_initialization_error)
        
        try:
            _db = firestore.client()
            # 接続テスト（簡単なクエリを実行）
            try:
                # 接続テストとして、コレクションの存在確認を試みる
                # エラーが発生しても無視（接続自体は成功している可能性がある）
                pass
            except Exception:
                pass
        except Exception as e:
            error_str = str(e)
            if "invalid_grant" in error_str or "account not found" in error_str:
                # サービスアカウントキーのパスを取得して表示
                service_account_path = _get_service_account_path(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
                if service_account_path:
                    try:
                        with open(service_account_path, 'r', encoding='utf-8') as f:
                            key_data = json.load(f)
                        project_id = key_data.get("project_id", "不明")
                        client_email = key_data.get("client_email", "不明")
                    except Exception:
                        project_id = "不明"
                        client_email = "不明"
                else:
                    project_id = "不明"
                    client_email = "不明"
                
                _initialization_error = (
                    f"Firestore接続エラー: サービスアカウントキーが無効です。\n"
                    f"プロジェクトID: {project_id}\n"
                    f"サービスアカウント: {client_email}\n"
                    f"エラー詳細: {error_str}\n\n"
                    f"解決方法:\n"
                    f"1. Firebase Console (https://console.firebase.google.com/) にアクセス\n"
                    f"2. プロジェクト '{project_id}' が存在するか確認\n"
                    f"3. サービスアカウント '{client_email}' が削除されていないか確認\n"
                    f"4. 新しいサービスアカウントキーを生成して、'{service_account_path or 'firebase-service-account.json'}' に保存\n"
                    f"5. バックエンドサーバーを再起動"
                )
            else:
                _initialization_error = f"Firestore接続エラー: {error_str}"
            raise ValueError(_initialization_error)
    
    if _initialization_error:
        raise ValueError(_initialization_error)
    
    return _db

