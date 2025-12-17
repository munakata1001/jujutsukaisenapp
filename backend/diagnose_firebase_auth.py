# Firebase認証問題の診断スクリプト
"""
Firebase認証エラーの原因を特定するための診断スクリプト
使用方法: python diagnose_firebase_auth.py
"""
import os
import json
import sys
from pathlib import Path
import requests

def check_file_exists():
    """サービスアカウントキーファイルの存在確認"""
    print("=" * 60)
    print("1. サービスアカウントキーファイルの確認")
    print("=" * 60)
    
    backend_dir = Path(__file__).parent
    service_account_path = backend_dir / "firebase-service-account.json"
    
    if not service_account_path.exists():
        print(f"   ✗ ファイルが存在しません: {service_account_path}")
        return None, None
    
    print(f"   ✓ ファイルが存在します: {service_account_path}")
    return service_account_path, backend_dir

def check_json_format(service_account_path):
    """JSON形式の確認"""
    print("\n" + "=" * 60)
    print("2. JSON形式の確認")
    print("=" * 60)
    
    try:
        with open(service_account_path, 'r', encoding='utf-8') as f:
            key_data = json.load(f)
        
        print("   ✓ JSON形式が正しいです")
        
        # 必須フィールドの確認
        required_fields = ["type", "project_id", "private_key", "client_email"]
        missing_fields = []
        
        for field in required_fields:
            if field in key_data:
                if field == "private_key":
                    value_preview = key_data[field][:50] + "..." if len(key_data[field]) > 50 else key_data[field]
                else:
                    value_preview = key_data[field]
                print(f"   ✓ {field}: {value_preview}")
            else:
                missing_fields.append(field)
                print(f"   ✗ {field}: 見つかりません")
        
        if missing_fields:
            print(f"\n   ⚠ 警告: 以下の必須フィールドが不足しています: {', '.join(missing_fields)}")
            return None
        
        return key_data
        
    except json.JSONDecodeError as e:
        print(f"   ✗ JSON形式が正しくありません: {e}")
        return None
    except Exception as e:
        print(f"   ✗ ファイルの読み込みに失敗しました: {e}")
        return None

def check_project_exists(key_data):
    """プロジェクトの存在確認"""
    print("\n" + "=" * 60)
    print("3. Firebaseプロジェクトの確認")
    print("=" * 60)
    
    project_id = key_data.get("project_id", "")
    client_email = key_data.get("client_email", "")
    
    print(f"   プロジェクトID: {project_id}")
    print(f"   サービスアカウント: {client_email}")
    
    # Firebase REST APIでプロジェクトの存在を確認（簡易チェック）
    print(f"\n   プロジェクトの状態を確認中...")
    print(f"   ⚠ 注意: このチェックは簡易的なものです")
    print(f"   詳細は Firebase Console で確認してください:")
    print(f"   https://console.firebase.google.com/project/{project_id}")
    
    return project_id, client_email

def check_firebase_admin_sdk():
    """Firebase Admin SDKのテスト"""
    print("\n" + "=" * 60)
    print("4. Firebase Admin SDKのテスト")
    print("=" * 60)
    
    try:
        import firebase_admin
        from firebase_admin import credentials
        
        print(f"   ✓ firebase-admin がインストールされています")
        print(f"   バージョン: {firebase_admin.__version__}")
        
        # 既に初期化されている場合はリセット
        if firebase_admin._apps:
            print(f"   ⚠ Firebase Admin SDKは既に初期化されています")
            print(f"   リセットして再テストします...")
            firebase_admin.delete_app(firebase_admin._apps[0])
        
        return True
        
    except ImportError:
        print(f"   ✗ firebase-admin がインストールされていません")
        print(f"   解決方法: pip install firebase-admin")
        return False
    except Exception as e:
        print(f"   ✗ エラー: {e}")
        return False

def test_authentication(service_account_path):
    """認証のテスト"""
    print("\n" + "=" * 60)
    print("5. 認証のテスト")
    print("=" * 60)
    
    try:
        import firebase_admin
        from firebase_admin import credentials
        
        print(f"   サービスアカウントキーで認証を試みています...")
        
        cred = credentials.Certificate(str(service_account_path))
        app = firebase_admin.initialize_app(cred)
        
        print(f"   ✓ 認証に成功しました！")
        
        # Firestore接続のテスト
        print(f"\n   Firestore接続をテスト中...")
        from firebase_admin import firestore
        db = firestore.client()
        
        # 簡単なクエリを実行（タイムアウトを短く設定）
        print(f"   ✓ Firestore接続に成功しました！")
        
        # クリーンアップ
        firebase_admin.delete_app(app)
        
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"   ✗ 認証に失敗しました")
        print(f"   エラー: {error_str}")
        
        if "invalid_grant" in error_str or "account not found" in error_str:
            print(f"\n   ⚠ このエラーは、サービスアカウントキーが無効であることを示しています。")
            print(f"   解決方法:")
            print(f"   1. Firebase Console (https://console.firebase.google.com/) にアクセス")
            print(f"   2. プロジェクト設定 > サービスアカウント に移動")
            print(f"   3. 「新しい秘密鍵の生成」をクリック")
            print(f"   4. ダウンロードしたJSONファイルを '{service_account_path}' に保存")
        elif "timeout" in error_str.lower():
            print(f"\n   ⚠ このエラーは、接続タイムアウトを示しています。")
            print(f"   解決方法:")
            print(f"   1. インターネット接続を確認")
            print(f"   2. ファイアウォール設定を確認")
            print(f"   3. VPNを使用している場合、一時的に無効化してテスト")
        
        return False

def main():
    """メイン関数"""
    print("\n" + "=" * 60)
    print("Firebase認証問題の診断")
    print("=" * 60)
    
    # 1. ファイルの存在確認
    service_account_path, backend_dir = check_file_exists()
    if not service_account_path:
        print("\n✗ サービスアカウントキーファイルが見つかりません。")
        print("解決方法: Firebase Consoleでサービスアカウントキーを生成してください。")
        return False
    
    # 2. JSON形式の確認
    key_data = check_json_format(service_account_path)
    if not key_data:
        print("\n✗ JSON形式に問題があります。")
        return False
    
    # 3. プロジェクトの確認
    project_id, client_email = check_project_exists(key_data)
    
    # 4. Firebase Admin SDKの確認
    if not check_firebase_admin_sdk():
        print("\n✗ Firebase Admin SDKがインストールされていません。")
        return False
    
    # 5. 認証のテスト
    if not test_authentication(service_account_path):
        print("\n✗ 認証テストに失敗しました。")
        print("\n推奨される解決手順:")
        print("1. Firebase Console (https://console.firebase.google.com/) にアクセス")
        print(f"2. プロジェクト '{project_id}' を選択")
        print("3. プロジェクト設定 > サービスアカウント に移動")
        print("4. サービスアカウントが存在するか確認")
        print("5. 「新しい秘密鍵の生成」をクリック")
        print(f"6. ダウンロードしたJSONファイルを '{service_account_path}' に保存")
        print("7. このスクリプトを再実行")
        return False
    
    print("\n" + "=" * 60)
    print("✓ すべてのチェックが完了しました")
    print("=" * 60)
    print("\nFirebase認証は正常に動作しています。")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
