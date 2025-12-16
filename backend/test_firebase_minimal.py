# Firebase最小構成のテストスクリプト
"""
Firebase最小構成を使用したテストデータの送受信テスト
使用方法: python test_firebase_minimal.py
"""
import sys
from datetime import datetime
from app.utils.firebase_minimal import get_firestore_db


def test_write_read():
    """書き込みと読み込みのテスト"""
    print("=" * 60)
    print("Firebase最小構成 - テストデータ送受信")
    print("=" * 60)
    
    try:
        # 1. Firestore接続
        print("\n[1] Firestoreに接続中...")
        db = get_firestore_db()
        print("    ✓ 接続成功")
        
        # 2. テストデータの作成
        print("\n[2] テストデータを作成中...")
        test_collection = "test_minimal"
        test_doc_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        test_data = {
            "message": "Hello Firebase!",
            "timestamp": datetime.now().isoformat(),
            "number": 123,
            "status": "active"
        }
        
        print(f"    コレクション: {test_collection}")
        print(f"    ドキュメントID: {test_doc_id}")
        print(f"    データ: {test_data}")
        
        # 3. データの書き込み
        print("\n[3] データを書き込み中...")
        doc_ref = db.collection(test_collection).document(test_doc_id)
        doc_ref.set(test_data)
        print("    ✓ 書き込み成功")
        
        # 4. データの読み込み
        print("\n[4] データを読み込み中...")
        doc = doc_ref.get()
        
        if not doc.exists:
            print("    ✗ エラー: ドキュメントが見つかりません")
            return False
        
        read_data = doc.to_dict()
        print("    ✓ 読み込み成功")
        print(f"    読み込んだデータ: {read_data}")
        
        # 5. データの検証
        print("\n[5] データの整合性を確認中...")
        if read_data.get("message") == test_data["message"]:
            print("    ✓ データの整合性が確認できました")
        else:
            print("    ✗ エラー: データの整合性に問題があります")
            return False
        
        # 6. データの更新
        print("\n[6] データを更新中...")
        update_data = {
            "status": "updated",
            "updated_at": datetime.now().isoformat()
        }
        doc_ref.update(update_data)
        print("    ✓ 更新成功")
        
        # 更新後の確認
        updated_doc = doc_ref.get()
        updated_data = updated_doc.to_dict()
        if updated_data.get("status") == "updated":
            print("    ✓ 更新が正しく反映されました")
        else:
            print("    ✗ エラー: 更新が正しく反映されていません")
            return False
        
        # 7. データの削除
        print("\n[7] データを削除中...")
        doc_ref.delete()
        
        # 削除確認
        deleted_doc = doc_ref.get()
        if not deleted_doc.exists:
            print("    ✓ 削除成功")
        else:
            print("    ✗ エラー: 削除に失敗しました")
            return False
        
        print("\n" + "=" * 60)
        print("✓ すべてのテストが成功しました！")
        print("=" * 60)
        print("\nFirebase最小構成は正常に動作しています。")
        return True
        
    except FileNotFoundError as e:
        print(f"\n✗ エラー: {e}")
        return False
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_write_read()
    sys.exit(0 if success else 1)
