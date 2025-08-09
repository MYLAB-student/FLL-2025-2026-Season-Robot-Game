# LEGO SPIKE Prime ロボット制御プログラム（Gemini-2.5-pro）

このプロジェクトは、LEGO SPIKE PrimeロボットをPybricksを使用して制御するためのPythonプログラム群です。

## 📁 プロジェクト構成

```
名称未設定フォルダ/
├── README.md              # このファイル
├── setup.py              # ロボット初期化モジュール
├── run.py                # 基本動作関数
├── selecter.py           # プログラム選択・実行インターフェース
└── straight_test.py      # 直進・回転テストプログラム
```

## 🚀 機能

### 主要機能
- **ロボット初期化**: ハブ、モーター、センサーの自動設定
- **PID制御**: 高精度な直進・回転制御
- **プログラム選択**: ボタン操作によるプログラム切り替え
- **センサーログ**: リアルタイムでのセンサー値表示
- **非同期処理**: 複数タスクの並行実行

### 動作関数
- `straight_with_power()`: 指定した出力で直進
- `turn_with_power()`: 指定した出力で回転
- `sensor_logger_task()`: センサー値の継続ログ出力

## 🔧 セットアップ

### 必要な環境
- LEGO SPIKE Prime ハブ
- Pybricks Firmware（最新版推奨）
- 2つのモーター（Port F, Port B）
- フォースセンサー（Port C、オプション）

### ハードウェア設定
```
Port F: 左モーター（反時計回り）
Port B: 右モーター（時計回り）
Port C: フォースセンサー（プログラム選択用）
```

### ロボット仕様
- ホイール直径: 56mm
- 車軸間距離: 115mm
- 最大速度: 500mm/s（直進）、500deg/s（回転）

## 📖 使用方法

### 1. 基本実行

#### 1.1 ロボットの初期化
```python
from setup import initialize_robot

# デフォルト設定で初期化
hub, left, right, robot = initialize_robot()

# カスタム設定で初期化
hub, left, right, robot = initialize_robot(
    straight_speed_percent=50,    # 直進速度50%
    turn_speed_percent=40,        # 旋回速度40%
    motor_power_percent=80        # モーターパワー80%
)
```

#### 1.2 基本動作の実行
```python
from run import straight_with_power, turn_with_power

# 直進動作
straight_with_power(robot, 100, 50)   # 100mm直進、出力50%
straight_with_power(robot, 200, 100)  # 200mm直進、最大出力
straight_with_power(robot, 50, 20)    # 50mm直進、低出力

# 回転動作
turn_with_power(robot, hub, 90, 30)   # 90度右回転、出力30%
turn_with_power(robot, hub, 180, 50)  # 180度回転、出力50%
turn_with_power(robot, hub, 360, 10)  # 360度回転、低出力
```

#### 1.3 連続動作の実行
```python
# 複数の動作を連続実行
def run_sequence():
    # 正方形を描く
    for i in range(4):
        straight_with_power(robot, 100, 60)  # 100mm直進
        turn_with_power(robot, hub, 90, 40)  # 90度回転
        wait(500)  # 0.5秒待機

# 実行
run_sequence()
```

### 2. プログラム選択モード

#### 2.1 セレクターの起動
```bash
# selecter.pyを実行
python selecter.py
```

#### 2.2 操作方法
| 操作 | 機能 |
|------|------|
| **LEFTボタン** | 前のプログラムに切り替え |
| **RIGHTボタン** | 次のプログラムに切り替え |
| **フォースセンサー** | 選択したプログラムを実行 |
| **ハブディスプレイ** | 現在のプログラム番号を表示 |

#### 2.3 プログラムリストの確認
```python
# selecter.py内のprogramsリスト
programs = [
    {"name": "直進テスト", "module": run, "function": "straight_with_power", "params": [robot, 100, 50]},
    {"name": "低速直進", "module": run, "function": "straight_with_power", "params": [robot, 100, 10]},
    {"name": "回転テスト", "module": run, "function": "turn_with_power", "params": [robot, hub, 100, 10]},
    # 新しいプログラムをここに追加
]
```

#### 2.4 新しいプログラムの追加
```python
# selecter.pyのprogramsリストに追加
{"name": "カスタム動作", "module": run, "function": "custom_function", "params": [robot, hub, parameter]}
```

### 3. テスト実行

#### 3.1 直進・回転テスト
```bash
# straight_test.pyを実行
python straight_test.py
```

**テスト内容:**
- 100mm直進（出力100%）
- 100mm直進（出力10%）
- 100度回転（出力100%）
- 360度回転（出力10%）

#### 3.2 センサーログの確認
```python
# リアルタイムでセンサー値を確認
async def sensor_logger_task():
    while True:
        heading = hub.imu.heading()
        left_deg = left.angle()
        right_deg = right.angle()
        dist = robot.distance()
        print(f"LOG: dist={dist:4.0f} mm  heading={heading:4.0f}°  L={left_deg:5.0f}°  R={right_deg:5.0f}°")
        await wait(200)
```

### 4. 非同期処理の活用

#### 4.1 複数タスクの並行実行
```python
from pybricks.tools import multitask, run_task

async def main_sequence():
    # メインの動作シーケンス
    await straight_with_power(robot, 200, 60)
    await turn_with_power(robot, hub, 90, 40)

# センサーログとメインシーケンスを並行実行
run_task(multitask(
    sensor_logger_task(),    # センサーログ
    main_sequence()          # メイン動作
))
```

#### 4.2 カスタム非同期関数の作成
```python
async def custom_sequence():
    """カスタム動作シーケンス"""
    print("カスタムシーケンス開始")
    
    # 複数の動作を順次実行
    await straight_with_power(robot, 150, 70)
    await wait(1000)  # 1秒待機
    
    await turn_with_power(robot, hub, 180, 50)
    await wait(500)   # 0.5秒待機
    
    await straight_with_power(robot, 150, 70)
    
    print("カスタムシーケンス完了")

# 実行
run_task(multitask(
    sensor_logger_task(),
    custom_sequence()
))
```

### 5. デバッグとトラブルシューティング

#### 5.1 ロボットの状態確認
```python
def check_robot_status():
    """ロボットの状態を確認"""
    print(f"左モーター角度: {left.angle()}°")
    print(f"右モーター角度: {right.angle()}°")
    print(f"走行距離: {robot.distance()} mm")
    print(f"現在の向き: {hub.imu.heading()}°")
    print(f"バッテリー残量: {hub.battery.voltage()} mV")

# 状態確認
check_robot_status()
```

#### 5.2 エラーハンドリング
```python
def safe_robot_operation():
    """安全なロボット操作"""
    try:
        # ロボットの初期化
        hub, left, right, robot = initialize_robot()
        
        # 動作実行
        straight_with_power(robot, 100, 50)
        turn_with_power(robot, hub, 90, 30)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # ロボットを停止
        robot.stop()
        robot.reset()
        hub.imu.reset_heading(0)
        print("ロボットをリセットしました")
```

#### 5.3 パフォーマンステスト
```python
def performance_test():
    """ロボットの性能テスト"""
    print("=== 性能テスト開始 ===")
    
    # 直進精度テスト
    print("1. 直進精度テスト")
    robot.reset()
    straight_with_power(robot, 100, 50)
    actual_distance = robot.distance()
    print(f"目標距離: 100mm, 実際の距離: {actual_distance}mm")
    
    # 回転精度テスト
    print("2. 回転精度テスト")
    hub.imu.reset_heading(0)
    turn_with_power(robot, hub, 90, 30)
    actual_heading = hub.imu.heading()
    print(f"目標角度: 90°, 実際の角度: {actual_heading}°")
    
    print("=== 性能テスト完了 ===")
```

## ⚙️ 設定パラメータ

### 速度設定（setup.py）
```python
straight_speed_percent = 40    # 直進速度（最大値の40%）
turn_speed_percent = 30        # 旋回速度（最大値の30%）
motor_power_percent = 100      # モーターパワー（100%）
```

### PID制御パラメータ
```python
# 距離制御
DISTANCE_KP = 1000
DISTANCE_KI = 50
DISTANCE_KD = 10

# 方向制御
HEADING_KP = 2000
HEADING_KI = 50
HEADING_KD = 100
```

## 🔍 センサー情報

### ログ出力例
```
LOG: dist= 150 mm  heading=  45°  L=  180°  R=  180°
```

**表示項目:**
- `dist`: 走行距離（mm）
- `heading`: 現在の向き（度）
- `L`: 左モーター角度（度）
- `R`: 右モーター角度（度）

## 🛠️ カスタマイズ

### 新しい動作関数の追加
```python
# run.pyに新しい関数を追加
def custom_action(robot, parameter):
    # カスタム動作の実装
    pass
```

### プログラムリストへの追加
```python
# selecter.pyのprogramsリストに追加
{"name": "カスタム動作", "module": run, "function": "custom_action", "params": [robot, parameter]}
```

## ⚠️ 注意事項

1. **初期化**: プログラム実行前に必ずロボットを初期化してください
2. **リセット**: エラー発生時はロボットをリセットしてください
3. **センサー**: ジャイロセンサーの初期化を忘れずに行ってください
4. **非同期処理**: `run_task()`を使用して非同期タスクを適切に管理してください

## 🐛 トラブルシューティング

### よくある問題
- **直進精度が悪い**: PIDパラメータの調整が必要
- **モーターが逆回転**: `positive_direction`の設定を確認
- **センサー値が異常**: ジャイロセンサーのリセットを実行

### デバッグ方法
1. センサーログを確認
2. 各ステップで`print()`文を追加
3. エラーメッセージを確認

## 📝 ライセンス

このプロジェクトは教育目的で作成されています。

## 🤝 貢献

バグ報告や機能改善の提案は歓迎します。

---

**作成者**: AI Assistant (Gemini-2.5-pro)  
**最終更新**: 2024年 