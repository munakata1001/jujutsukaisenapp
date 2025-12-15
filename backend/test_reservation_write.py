# 予約データの書き込みテストスクリプト
"""
予約データをFirestoreに書き込むテストスクリプト
使用方法: python test_reservation_write.py
"""
import os
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

async def test_reservation_write():
    """予約データの書き込みをテスト"""
    print("=" * 60)
    print("予約データ書き込みテスト")
    print("=" * 60)
    
    try:
        # Firebase初期化
        from app.utils.firebase import get_firestore_db
        from app.services.reservation_service import create_reservation
        
        print("\n1. Firestore接続を確認中...")
        db = get_firestore_db()
        print("   ✓ Firestore接続に成功しました")
        
        # テスト用の予約枠を作成
        print("\n2. テスト用の予約枠を作成中...")
        from app.services.timeslot_service import create_timeslot, generate_slot_id, get_timeslot
        
        # 明日の日付を取得
        tomorrow = date.today() + timedelta(days=1)
        test_time = "10:00"
        
        slot_id = generate_slot_id(tomorrow, test_time)
        
        # 既存の予約枠を確認
        existing_slot = await get_timeslot(slot_id)
        
        if not existing_slot:
            await create_timeslot(tomorrow, test_time, capacity=10)
            print(f"   ✓ 予約枠を作成しました: {tomorrow} {test_time}")
        else:
            print(f"   ✓ 予約枠が既に存在します: {tomorrow} {test_time}")
        
        # テスト用の予約データ
        print("\n3. テスト用の予約データを準備中...")
        reservation_data = {
            "user_email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "user_name": "テスト太郎",
            "user_phone": "09012345678",
            "visit_date": tomorrow,
            "visit_time": test_time,
            "products": [],  # 商品なしでテスト
        }
        
        print(f"   予約者名: {reservation_data['user_name']}")
        print(f"   メール: {reservation_data['user_email']}")
        print(f"   来店日時: {reservation_data['visit_date']} {reservation_data['visit_time']}")
        
        # 予約を作成
        print("\n4. 予約を作成中...")
        result = await create_reservation(reservation_data)
        
        print(f"   ✓ 予約の作成に成功しました！")
        print(f"   予約ID: {result.get('reservation_id')}")
        print(f"   予約番号: {result.get('reservation_number')}")
        print(f"   ステータス: {result.get('status')}")
        
        # 予約を確認
        print("\n5. 作成した予約を確認中...")
        from app.services.reservation_service import get_reservation_by_number
        
        reservation = await get_reservation_by_number(result.get('reservation_number'))
        
        if reservation:
            print(f"   ✓ 予約の確認に成功しました")
            print(f"   予約番号: {reservation.get('reservation_number')}")
            print(f"   予約者名: {reservation.get('user_name')}")
            print(f"   来店日時: {reservation.get('visit_date')} {reservation.get('visit_time')}")
        else:
            print(f"   ✗ 予約の確認に失敗しました")
            return False
        
        # 予約枠の予約済み数を確認
        print("\n6. 予約枠の状態を確認中...")
        updated_slot = await get_timeslot(slot_id)
        if updated_slot:
            reserved_count = updated_slot.get('reserved_count', 0)
            capacity = updated_slot.get('capacity', 0)
            print(f"   ✓ 予約枠の状態を確認しました")
            print(f"   定員: {capacity}")
            print(f"   予約済み: {reserved_count}")
            print(f"   空き: {capacity - reserved_count}")
        
        print(f"\n" + "=" * 60)
        print(f"✓ 予約データの書き込みテストが成功しました！")
        print(f"=" * 60)
        print(f"\n予約番号: {result.get('reservation_number')}")
        print(f"この予約番号で予約を確認できます。")
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"\n✗ エラーが発生しました: {error_str}")
        
        if "invalid_grant" in error_str or "account not found" in error_str:
            print(f"\n⚠ このエラーは、Firebase認証の問題を示しています。")
            print(f"解決方法:")
            print(f"1. Firebase Consoleで新しいサービスアカウントキーを生成してください")
            print(f"2. backend/firebase-service-account.json に保存してください")
        elif "満席" in error_str or "予約枠" in error_str:
            print(f"\n⚠ 予約枠の問題です。")
            print(f"解決方法:")
            print(f"1. 管理者画面で予約枠を作成してください")
            print(f"2. または、test_reservation_write.pyの日時を変更してください")
        else:
            print(f"\nエラーの詳細:")
            import traceback
            traceback.print_exc()
        
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_reservation_write())
    sys.exit(0 if success else 1)

