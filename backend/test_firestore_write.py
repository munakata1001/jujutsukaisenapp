# Firestore書き込みテストスクリプト
"""
Firestoreへの書き込み・読み込み・削除をテストするスクリプト
使用方法: python test_firestore_write.py
"""
import os
import sys
from datetime import datetime
from pathlib import Path

def test_firestore_write():
    """Firestoreへの書き込みをテスト"""
    print("=" * 60)
    print("Firestore書き込みテスト")
    print("=" * 60)
    
    try:
        # Firebase初期化
        from app.utils.firebase import get_firestore_db
        
        print("\n1. Firestore接続を確認中...")
        db = get_firestore_db()
        print("   ✓ Firestore接続に成功しました")
        
        # テストデータの準備
        test_collection = "test_reservations"
        test_doc_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        test_data = {
            "test_id": test_doc_id,
            "test_name": "テスト予約",
            "test_email": "test@example.com",
            "test_date": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }
        
        print(f"\n2. テストデータを作成中...")
        print(f"   コレクション: {test_collection}")
        print(f"   ドキュメントID: {test_doc_id}")
        print(f"   データ: {test_data}")
        
        # 書き込みテスト
        print(f"\n3. Firestoreへの書き込みをテスト中...")
        doc_ref = db.collection(test_collection).document(test_doc_id)
        doc_ref.set(test_data)
        print(f"   ✓ 書き込みに成功しました")
        
        # 読み込みテスト
        print(f"\n4. Firestoreからの読み込みをテスト中...")
        doc = doc_ref.get()
        
        if doc.exists:
            read_data = doc.to_dict()
            print(f"   ✓ 読み込みに成功しました")
            print(f"   読み込んだデータ: {read_data}")
            
            # データの検証
            if read_data.get("test_id") == test_doc_id:
                print(f"   ✓ データの整合性が確認できました")
            else:
                print(f"   ✗ データの整合性に問題があります")
                return False
        else:
            print(f"   ✗ ドキュメントが見つかりませんでした")
            return False
        
        # 更新テスト
        print(f"\n5. Firestoreの更新をテスト中...")
        update_data = {
            "updated_at": datetime.now().isoformat(),
            "test_status": "updated"
        }
        doc_ref.update(update_data)
        
        # 更新後のデータを確認
        updated_doc = doc_ref.get()
        if updated_doc.exists:
            updated_data = updated_doc.to_dict()
            if updated_data.get("test_status") == "updated":
                print(f"   ✓ 更新に成功しました")
                print(f"   更新後のデータ: {updated_data}")
            else:
                print(f"   ✗ 更新が正しく反映されていません")
                return False
        else:
            print(f"   ✗ 更新後のドキュメントが見つかりませんでした")
            return False
        
        # 削除テスト
        print(f"\n6. Firestoreからの削除をテスト中...")
        doc_ref.delete()
        
        # 削除後の確認
        deleted_doc = doc_ref.get()
        if not deleted_doc.exists:
            print(f"   ✓ 削除に成功しました")
        else:
            print(f"   ✗ 削除が正しく実行されていません")
            return False
        
        # クエリテスト
        print(f"\n7. Firestoreのクエリをテスト中...")
        
        # テスト用の複数ドキュメントを作成
        test_docs = []
        for i in range(3):
            doc_id = f"test_query_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            doc_data = {
                "test_id": doc_id,
                "test_name": f"テスト予約{i}",
                "test_index": i,
                "created_at": datetime.now().isoformat(),
            }
            db.collection(test_collection).document(doc_id).set(doc_data)
            test_docs.append(doc_id)
        
        print(f"   テスト用ドキュメントを3件作成しました")
        
        # クエリで取得
        from google.cloud.firestore_v1 import FieldFilter
        query = db.collection(test_collection).where(
            filter=FieldFilter("test_index", ">=", 0)
        ).limit(10)
        
        docs = list(query.stream())
        print(f"   ✓ クエリで{len(docs)}件のドキュメントを取得しました")
        
        # テスト用ドキュメントを削除
        for doc_id in test_docs:
            db.collection(test_collection).document(doc_id).delete()
        print(f"   テスト用ドキュメントを削除しました")
        
        print(f"\n" + "=" * 60)
        print(f"✓ すべてのテストが成功しました！")
        print(f"=" * 60)
        print(f"\nFirestoreへの書き込み・読み込み・更新・削除・クエリが正常に動作しています。")
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"\n✗ エラーが発生しました: {error_str}")
        
        if "invalid_grant" in error_str or "account not found" in error_str:
            print(f"\n⚠ このエラーは、Firebase認証の問題を示しています。")
            print(f"解決方法:")
            print(f"1. Firebase Consoleで新しいサービスアカウントキーを生成してください")
            print(f"2. backend/firebase-service-account.json に保存してください")
            print(f"3. python check_firebase_config.py を実行して設定を確認してください")
        elif "timeout" in error_str.lower():
            print(f"\n⚠ このエラーは、Firestoreへの接続タイムアウトを示しています。")
            print(f"解決方法:")
            print(f"1. インターネット接続を確認してください")
            print(f"2. ファイアウォール設定を確認してください")
        else:
            print(f"\nエラーの詳細:")
            import traceback
            traceback.print_exc()
        
        return False

if __name__ == "__main__":
    success = test_firestore_write()
    sys.exit(0 if success else 1)



