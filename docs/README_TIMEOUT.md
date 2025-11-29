# タイムアウト機能の使い方ガイド

## 概要

ロボットが壁にぶつかったり、想定外の状況で停止した場合でも、指定した時間が経過したら自動的に次の行動に移るためのタイムアウト機能です。

## 問題点

従来のコードでは以下のような問題がありました：

```python
# 壁にぶつかると、ここで永遠に待ち続けてしまう
await robot.straight(500)
# 次の動作に進まない...
```

また、タイムアウトを実装しようとすると、毎回以下のような長いコードを書く必要がありました：

```python
robot.straight(205, wait=False)
timeout = StopWatch()
timeout.reset()
while timeout.time() < 3000:
    if not robot.done():
        await wait(10)
    else:
        break
```

## 解決策

`template_timeout.py` を使うことで、簡潔にタイムアウト機能を実装できます。

## 基本的な使い方

### 1. インポート

```python
from template_timeout import safe_straight, safe_turn, safe_motor_angle, safe_curve
```

### 2. 直進動作（safe_straight）

```python
# 500mm直進、3秒でタイムアウト
await safe_straight(robot, 500, timeout_ms=3000)

# 壁にぶつかっても3秒後には次の動作に進む
```

### 3. 回転動作（safe_turn）

```python
# 90度回転、2秒でタイムアウト
await safe_turn(robot, 90, timeout_ms=2000)
```

### 4. モーター動作（safe_motor_angle）

```python
# 左リフトを300速度で180度回転、2秒でタイムアウト
await safe_motor_angle(left_lift, 300, 180, timeout_ms=2000, motor_name="左リフト")

# 右リフトも同様
await safe_motor_angle(right_lift, 500, -360, timeout_ms=2000, motor_name="右リフト")
```

### 5. カーブ動作（safe_curve）

```python
# 半径200mmで90度カーブ、3秒でタイムアウト
await safe_curve(robot, 200, 90, timeout_ms=3000)
```

## 実際の使用例

### Before（従来のコード）

```python
# run1_M01_M02_kanna.py の一部
robot.straight(205, wait=False)  #まっすぐすすむ（非ブロッキング）
timeout = StopWatch()  # タイマーを作成
timeout.reset()  # タイマーをリセット
while timeout.time() < 3000:  # 3000ミリ秒（3秒）までループ
    # 直進動作が完了したかチェック
    if not robot.done():
        await wait(10)  # まだ動作中の場合、10ミリ秒待機してから再チェック
    else:
        break
```

### After（タイムアウト機能使用）

```python
from template_timeout import safe_straight

# たった1行で同じことができる！
await safe_straight(robot, 205, timeout_ms=3000)
```

## 完全なコード例

### M01, M02ミッション

```python
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task
from setup import initialize_robot

# タイムアウト機能をインポート
from template_timeout import safe_straight, safe_turn, safe_motor_angle


async def run(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    # M01ミッション
    await safe_straight(robot, 590, timeout_ms=4000)   # 前進
    await safe_straight(robot, -120, timeout_ms=2000)  # 後進
    
    # M02ミッション
    await safe_turn(robot, 40, timeout_ms=2000)        # 回転
    await safe_straight(robot, 220, timeout_ms=3000)   # 前進
    await safe_turn(robot, -85, timeout_ms=2000)       # 回転
    
    # 壁にぶつかる可能性がある動作（短めのタイムアウト）
    await safe_straight(robot, 205, timeout_ms=2000)
    
    # アーム操作
    await safe_motor_angle(left_lift, 300, 180, timeout_ms=2000, motor_name="左リフト")
    
    print("ミッション完了！")


async def main():
    await run(hub, robot, left_wheel, right_wheel, left_lift, right_lift)


if __name__ == "__main__":
    hub, robot, left_wheel, right_wheel, left_lift, right_lift = initialize_robot()
    run_task(main())
```

## タイムアウト時間の目安

- **短距離移動（～200mm）**: 2000ms（2秒）
- **中距離移動（200～500mm）**: 3000ms（3秒）
- **長距離移動（500mm～）**: 4000～5000ms（4～5秒）
- **回転動作**: 1500～2000ms（1.5～2秒）
- **アーム・リフト操作**: 2000～3000ms（2～3秒）
- **壁にぶつかる可能性が高い動作**: 短めに設定（1500～2000ms）

## 高度な使い方

### 動作が成功したかチェック

```python
# 動作が成功したかどうかを確認できる
success = await safe_straight(robot, 500, timeout_ms=3000)

if success:
    print("動作完了！次の動作へ")
    await safe_turn(robot, 90, timeout_ms=2000)
else:
    print("タイムアウト！代替ルートへ")
    await safe_turn(robot, -90, timeout_ms=2000)
```

### wait_with_timeout（低レベルAPI）

より細かい制御が必要な場合：

```python
from template_timeout import wait_with_timeout

# 動作を非同期で開始
robot.straight(500, wait=False)

# タイムアウト付きで待機
success = await wait_with_timeout(robot, timeout_ms=3000, check_interval_ms=10)
```

## サンプルファイル

実際に動作するサンプルファイルが用意されています：

- `run1_M01_M02_kanna_with_timeout.py` - M01, M02ミッションの例
- `run1_M08_M06_M05_with_timeout.py` - M08, M06, M05ミッションの例

これらのファイルを参考にして、自分のミッションプログラムに適用してください。

## 既存コードの置き換え方法

### ステップ1: インポート追加

ファイルの先頭に以下を追加：

```python
from template_timeout import safe_straight, safe_turn, safe_motor_angle, safe_curve
```

### ステップ2: 動作を置き換え

| Before | After |
|--------|-------|
| `await robot.straight(500)` | `await safe_straight(robot, 500, timeout_ms=3000)` |
| `await robot.turn(90)` | `await safe_turn(robot, 90, timeout_ms=2000)` |
| `await left_lift.run_angle(300, 180)` | `await safe_motor_angle(left_lift, 300, 180, timeout_ms=2000, motor_name="左リフト")` |
| `await robot.curve(200, 90)` | `await safe_curve(robot, 200, 90, timeout_ms=3000)` |

### ステップ3: タイムアウト時間を調整

実際のロボットでテストしながら、適切なタイムアウト時間を調整してください。

## トラブルシューティング

### Q: タイムアウトが頻繁に発生する

A: タイムアウト時間を長くするか、ロボットの速度設定を確認してください。

```python
# タイムアウト時間を延ばす
await safe_straight(robot, 500, timeout_ms=5000)  # 3秒→5秒に変更
```

### Q: タイムアウト機能を使いたくない動作がある

A: 通常の `await robot.straight()` などを使用してください。混在して使えます。

```python
# タイムアウトあり
await safe_straight(robot, 500, timeout_ms=3000)

# タイムアウトなし（従来通り）
await robot.straight(200)
```

### Q: モーター名を日本語にしたい

A: `motor_name` パラメータに日本語を指定できます。

```python
await safe_motor_angle(left_lift, 300, 180, timeout_ms=2000, motor_name="左側アーム")
```

## まとめ

- ✅ 壁にぶつかっても自動的に次の動作に進む
- ✅ コードが簡潔になる（1行で記述可能）
- ✅ タイムアウト時間を簡単に調整できる
- ✅ 既存のコードと混在して使える
- ✅ 動作の成功/失敗を判定できる

タイムアウト機能を活用して、より安定したロボットプログラムを作成しましょう！

