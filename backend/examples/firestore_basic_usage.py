# Firestore基本的な使い方の例
"""
Firestoreの基本的な操作を実演するサンプルコード
"""
from datetime import datetime
from app.utils.firebase import get_firestore_db
from google.cloud.firestore_v1 import FieldFilter

def example_create():
    """データの作成例"""
    print("=" * 60)
    print("1. データの作成")
    print("=" * 60)
    
    db = get_firestore_db()
    
    # データを準備
    data = {
        "name": "サンプルデータ",
        "email": "sample@example.com",
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    # ドキュメントIDを自動生成
    doc_ref = db.collection("examples").document()
    doc_ref.set(data)
    
    print(f"✓ データを作成しました")
    print(f"  ドキュメントID: {doc_ref.id}")
    print(f"  データ: {data}")
    
    return doc_ref.id

def example_read(doc_id: str):
    """データの読み込み例"""
    print("\n" + "=" * 60)
    print("2. データの読み込み")
    print("=" * 60)
    
    db = get_firestore_db()
    
    # ドキュメントを取得
    doc_ref = db.collection("examples").document(doc_id)
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        print(f"✓ データを読み込みました")
        print(f"  ドキュメントID: {doc.id}")
        print(f"  データ: {data}")
        return data
    else:
        print(f"✗ ドキュメントが見つかりません")
        return None

def example_update(doc_id: str):
    """データの更新例"""
    print("\n" + "=" * 60)
    print("3. データの更新")
    print("=" * 60)
    
    db = get_firestore_db()
    
    # データを更新
    doc_ref = db.collection("examples").document(doc_id)
    doc_ref.update({
        "updated_at": datetime.now().isoformat(),
        "status": "updated"
    })
    
    print(f"✓ データを更新しました")
    
    # 更新後のデータを確認
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        print(f"  更新後のデータ: {data}")

def example_query():
    """クエリの例"""
    print("\n" + "=" * 60)
    print("4. クエリ（検索）")
    print("=" * 60)
    
    db = get_firestore_db()
    
    # 条件で検索
    query = db.collection("examples").where(
        filter=FieldFilter("status", "==", "active")
    ).limit(10)
    
    docs = list(query.stream())
    print(f"✓ {len(docs)}件のドキュメントを取得しました")
    
    for doc in docs:
        data = doc.to_dict()
        print(f"  - {doc.id}: {data.get('name', 'N/A')}")

def example_delete(doc_id: str):
    """データの削除例"""
    print("\n" + "=" * 60)
    print("5. データの削除")
    print("=" * 60)
    
    db = get_firestore_db()
    
    # ドキュメントを削除
    doc_ref = db.collection("examples").document(doc_id)
    doc_ref.delete()
    
    print(f"✓ データを削除しました")
    
    # 削除確認
    doc = doc_ref.get()
    if not doc.exists:
        print(f"✓ 削除が確認されました")
    else:
        print(f"✗ 削除に失敗しました")

def example_batch_write():
    """バッチ書き込みの例"""
    print("\n" + "=" * 60)
    print("6. バッチ書き込み")
    print("=" * 60)
    
    db = get_firestore_db()
    
    # バッチオブジェクトを作成
    batch = db.batch()
    
    # 複数のドキュメントを追加
    for i in range(3):
        doc_ref = db.collection("examples").document()
        data = {
            "name": f"バッチデータ{i}",
            "index": i,
            "created_at": datetime.now().isoformat()
        }
        batch.set(doc_ref, data)
    
    # バッチをコミット
    batch.commit()
    
    print(f"✓ 3件のデータをバッチで作成しました")

def main():
    """メイン関数"""
    try:
        # 1. 作成
        doc_id = example_create()
        
        # 2. 読み込み
        data = example_read(doc_id)
        
        if data:
            # 3. 更新
            example_update(doc_id)
            
            # 4. クエリ
            example_query()
            
            # 5. 削除
            example_delete(doc_id)
        
        # 6. バッチ書き込み
        example_batch_write()
        
        print("\n" + "=" * 60)
        print("✓ すべての例が完了しました")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()



