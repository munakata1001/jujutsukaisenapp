# Firebase設定確認スクリプト
"""
Firebase設定を確認するための診断スクリプト
使用方法: python check_firebase_config.py
"""
import os
import json
import sys
from pathlib import Path

def check_firebase_config():
    """Firebase設定を確認"""
    print("=" * 60)
    print("Firebase設定確認")
    print("=" * 60)
    
    # 1. サービスアカウントキーファイルの確認
    backend_dir = Path(__file__).parent
    service_account_path = backend_dir / "firebase-service-account.json"
    
    print(f"\n1. サービスアカウントキーファイルの確認")
    print(f"   パス: {service_account_path}")
    
    if service_account_path.exists():
        print(f"   ✓ ファイルが存在します")
        
        try:
            with open(service_account_path, 'r', encoding='utf-8') as f:
                key_data = json.load(f)
            
            print(f"   ✓ JSON形式が正しいです")
            
            # 必須フィールドの確認
            required_fields = ["type", "project_id", "private_key", "client_email"]
            missing_fields = []
            
            for field in required_fields:
                if field in key_data:
                    print(f"   ✓ {field}: {key_data[field][:50] if len(str(key_data[field])) > 50 else key_data[field]}...")
                else:
                    missing_fields.append(field)
                    print(f"   ✗ {field}: 見つかりません")
            
            if missing_fields:
                print(f"\n   ⚠ 警告: 以下の必須フィールドが不足しています: {', '.join(missing_fields)}")
            else:
                print(f"\n   ✓ すべての必須フィールドが存在します")
            
            # プロジェクトIDとサービスアカウントの表示
            project_id = key_data.get("project_id", "不明")
            client_email = key_data.get("client_email", "不明")
            
            print(f"\n   プロジェクトID: {project_id}")
            print(f"   サービスアカウント: {client_email}")
            
        except json.JSONDecodeError as e:
            print(f"   ✗ JSON形式が正しくありません: {e}")
            return False
        except Exception as e:
            print(f"   ✗ ファイルの読み込みに失敗しました: {e}")
            return False
    else:
        print(f"   ✗ ファイルが存在しません")
        print(f"\n   解決方法:")
        print(f"   1. Firebase Console (https://console.firebase.google.com/) にアクセス")
        print(f"   2. プロジェクト設定 > サービスアカウント に移動")
        print(f"   3. 「新しい秘密鍵の生成」をクリック")
        print(f"   4. ダウンロードしたJSONファイルを '{service_account_path}' に保存")
        return False
    
    # 2. 環境変数の確認
    print(f"\n2. 環境変数の確認")
    google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if google_creds:
        print(f"   ✓ GOOGLE_APPLICATION_CREDENTIALS: {google_creds}")
    else:
        print(f"   - GOOGLE_APPLICATION_CREDENTIALS: 設定されていません（デフォルトパスを使用）")
    
    # 3. Firebase Admin SDKのテスト
    print(f"\n3. Firebase Admin SDKのテスト")
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        if firebase_admin._apps:
            print(f"   ⚠ Firebase Admin SDKは既に初期化されています")
        else:
            print(f"   Firebase Admin SDKを初期化中...")
            cred = credentials.Certificate(str(service_account_path))
            firebase_admin.initialize_app(cred)
            print(f"   ✓ Firebase Admin SDKの初期化に成功しました")
            
            # Firestore接続テスト
            print(f"   Firestore接続をテスト中...")
            db = firestore.client()
            print(f"   ✓ Firestore接続に成功しました")
            
    except Exception as e:
        error_str = str(e)
        print(f"   ✗ エラーが発生しました: {error_str}")
        
        if "invalid_grant" in error_str or "account not found" in error_str:
            print(f"\n   ⚠ このエラーは、サービスアカウントキーが無効であることを示しています。")
            print(f"   解決方法:")
            print(f"   1. Firebase Consoleで新しいサービスアカウントキーを生成してください")
            print(f"   2. サービスアカウントが削除されていないか確認してください")
            print(f"   3. プロジェクトIDが正しいか確認してください")
        
        return False
    
    print(f"\n" + "=" * 60)
    print(f"✓ すべてのチェックが完了しました")
    print(f"=" * 60)
    return True

if __name__ == "__main__":
    success = check_firebase_config()
    sys.exit(0 if success else 1)

