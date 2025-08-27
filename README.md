# LEGO SPIKE Prime ロボット制御プログラム（Gemini-2.5-pro）

このプロジェクトは、LEGO SPIKE PrimeロボットをPybricksを使用して制御するためのPythonプログラム群です。

## 📑 目次

- [📁 プロジェクト構成](#-プロジェクト構成)
- [⚡ 開発時の流れ](#-開発時の流れ)
  - [新しいランファイルの作成手順](#新しいランファイルの作成手順)
  - [selector.pyでの登録手順](#selectorpyでの登録手順)
- [⚡ 競技時の操作方法](#-競技時の操作方法)
- [🚀 機能](#-機能)
- [🔧 セットアップ](#-セットアップ)
- [📖 使用方法](#-使用方法)
- [⚙️ 設定パラメータ](#️-設定パラメータ)
- [🔍 センサー情報](#-センサー情報)
- [🛠️ カスタマイズ](#️-カスタマイズ)
- [⚠️ 注意事項](#️-注意事項)
- [🐛 トラブルシューティング](#-トラブルシューティング)

## 📁 プロジェクト構成

```
名称未設定フォルダ/
├── README.md              # このファイル
├── selecter.py           # プログラム選択・実行インターフェース
    ├── setup.py              # ロボット初期化モジュール
    ├── run1.py                # ランごとに作る実行ファイル
    ├── run2.py                
    ├── run3.py                
    └── straight_test.py      # 直進・回転テスト用プログラム


```
## ⚡ 開発時の流れ

### 新しいランファイルの作成手順

1. **ファイル名の決定**
   - `run●.py`の形式で作成（●は数字）
   - 例: `run2.py`, `run3.py`, `run4.py`など

2. **新しいrunファイルの作成**
   ```python
   # run2.py（例）
   from pybricks.hubs import PrimeHub
   from pybricks.parameters import Port, Axis, Direction
   from pybricks.pupdevices import Motor
   from pybricks.robotics import DriveBase
   from pybricks.tools import wait, multitask, run_task
   from setup import initialize_robot

   def run2(robot, hub, left, right, lift):
       """run2のミッション実行関数
       
       Args:
           robot: DriveBaseオブジェクト
           hub: PrimeHubオブジェクト  
           left: 左モーターオブジェクト
           right: 右モーターオブジェクト
           lift: リフトモーターオブジェクト
       """
       # ここにミッションの動作を記述
       robot.straight(200)  # 200mm直進
       robot.turn(90)       # 90度回転
       wait(500)           # 0.5秒待機
   ```

3. **ファイルの保存**
   - プロジェクトルートディレクトリに保存
   - 文字エンコーディングはUTF-8で保存

### selector.pyでの登録手順

1. **新しいrunファイルのインポート**
   ```python
   # selecter.pyの上部にインポート文を追加
   import run
   import run1
   import run2  # 新しく追加
   ```

2. **programsリストへの追加**
   ```python
   # selecter.pyのprogramsリストに新しいエントリを追加
   programs = [
       {"name": "straight_with_power", "module": run, "description": "straight_with_power関数", "function": "straight_with_power", "params": [robot,100, 50]},
       {"name": "straight_with_power", "module": run, "description": "straight_with_power関数", "function": "straight_with_power", "params": [robot,100, 10]},
       {"name": "回転", "module": run, "description": "回転", "function": "turn_with_power", "params": [robot,hub,100, 10]},
       {"name": "run1", "module": run1, "description": "run1関数", "function": "run1", "params": [robot,hub,left,right,lift]},
       {"name": "run2", "module": run2, "description": "run2関数", "function": "run2", "params": [robot,hub,left,right,lift]},  # 新しく追加
       # 他のプログラムをここに追加
   ]
   ```

3. **プログラムエントリの構成要素**
   - `name`: セレクター表示名（短くわかりやすく）
   - `module`: インポートしたモジュール名
   - `description`: 詳細説明（ターミナル表示用）
   - `function`: 実行する関数名（文字列）
   - `params`: 関数に渡すパラメータのリスト

4. **動作確認**
   - selecter.pyを実行してプログラムリストに表示されることを確認
   - ハブのボタンで選択し、フォースセンサーで実行テスト

5. **ハブへの書き込み**
   - Pybricks Appからselecter.pyをメインとしてハブにダウンロード
   - オフライン実行が可能になる

### 注意点
- runファイルの関数は必ず`robot, hub, left, right, lift`の5つの引数を受け取る形式にする
- インポート順序はselecter.pyで参照する順番に合わせる
- プログラム名は重複しないよう注意する



### ⚡ 競技時の操作方法

1) ハードウェア接続
- Port F: 左モーター（反時計回り）
- Port B: 右モーター（時計回り）
- Port C: フォースセンサー（選択/実行用）


2) 操作

#### スタート時

hubのメインボタンを長押しして起動し、実行するファイルの番号を選択して、フォースセンサーを押して実行

- LEFT: 前のプログラム
- RIGHT: 次のプログラム
- フォースセンサー（C）: 選択したプログラムを実行

4) 最短でミッションを1件登録（`selecter.py` の `programs` に追記）

```python
{"name": "M01 直進100mm(50%)", "module": run, "description": "M01 直進テスト", "function": "straight_with_power", "params": [robot, 100, 50]}
```

5) 新しいファイルでミッションを定義して登録
- 例: `missions_gemini_2_5_pro.py`を作成

```python
# missions_gemini_2_5_pro.py
from pybricks.tools import wait

def m01_bridge(robot, hub):
    #ここに処理を書く
    robot.settings()
    robot.straight(200)
    wait(200)
```

- `selecter.py` にインポートして登録

```python
import missions_gemini_2_5_pro

programs += [
    {"name": "M01 ブリッジ", "module": missions_gemini_2_5_pro, "description": "M01: 橋アプローチ", "function": "m01_bridge", "params": [robot, hub]},
]
```


ヒント
- 必須キー: `name`, `module`, `description`, `function`
- 多くの関数は `robot`/`hub` を使うため `params` で渡す
- 括弧入りファイル名は通常の `import` ができないため、必要なら本文の `importlib` 例を利用

7) 書き込み後は本体のみで動作します（オフライン実行）
- Pybricks App から `selecter.py` をメインとしてハブに「ダウンロード（保存）」してください
- 以後は PC 接続なしで、ハブの電源を入れて中央ボタンからプログラムを起動できます
- 本プロジェクトのセレクターは、ハブの左右ボタン／フォースセンサーで選択・実行できます

## 🚀 機能

### 主要機能
- **ロボット初期化**: ハブ、モーター、センサーの自動設定
- **PID制御**: 高精度な直進・回転制御
- **プログラム選択**: ボタン操作によるプログラム切り替え
- **センサーログ**: リアルタイムでのセンサー値表示
- **非同期処理**: 複数タスクの並行実行


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

#### 2.5 新しいファイルを作ってセレクターに登録する

新しい動作を別ファイルに切り出して管理したい場合の手順です。

- **ファイル名のルール（重要）**: Pythonでインポートできるように、英数字とアンダースコアのみを使用してください。
  - 例: `my_actions_gemini_2_5_pro.py`（括弧やハイフンは使わない）

1) 新しいファイルを作成（例: `my_actions_gemini_2_5_pro.py`）

```python
"""Generated with Gemini-2.5-pro"""

from pybricks.tools import wait

def straight_slow(robot, distance_mm: int, motor_power: int):
    robot.settings(straight_speed=abs(motor_power) * 5)
    robot.straight(distance_mm)
    wait(100)

def turn_and_go(robot, hub, angle_deg: int, distance_mm: int, motor_power: int):
    robot.settings(turn_rate=abs(motor_power) * 5)
    robot.turn(angle_deg)
    hub.imu.reset_heading(0)
    robot.settings(straight_speed=abs(motor_power) * 5)
    robot.straight(distance_mm)
```

2) `selecter.py` に新ファイルをインポート

```python
# ファイル先頭付近に追記
import my_actions_gemini_2_5_pro as my_actions
```

補足: ファイル名にモデル名を括弧付きで含めたい場合

- 例: `my_actions（Gemini-2.5-pro）.py` のように括弧やハイフンを含むと、`import my_actions（...）` のような通常のインポートはできません。
- この場合は `importlib` を使ってファイルパスから読み込みます（下記例ではモジュール名を `my_actions` に割り当て）。

```python
import importlib.util, sys

module_path = "my_actions（Gemini-2.5-pro）.py"
spec = importlib.util.spec_from_file_location("my_actions", module_path)
my_actions = importlib.util.module_from_spec(spec)
sys.modules["my_actions"] = my_actions
spec.loader.exec_module(my_actions)
```

3) `selecter.py` の `programs` リストに登録

```python
programs = [
    # 既存エントリ...
    {"name": "低速直進(新ファイル)", "module": my_actions, "description": "新ファイル: 低速直進", "function": "straight_slow", "params": [robot, 120, 20]},
    {"name": "回転→前進(新ファイル)", "module": my_actions, "description": "新ファイル: 回転後に前進", "function": "turn_and_go", "params": [robot, hub, 90, 150, 40]},
]
```

4) 実行して確認

```bash
python selecter.py
```

5) うまくいかない場合
- **ModuleNotFoundError**: ファイル名とインポート名が一致しているか（拡張子 `.py` を除いた名前）を確認
- **TypeError**: `params` の順番・個数が関数定義と一致しているか確認
- **NameError**: `module` に指定したオブジェクト名（例: `my_actions`）を正しくインポートしているか確認

#### 2.6 プログラムリストのフォーマット

`selecter.py` の `programs` は、以下の辞書要素のリストです。

```python
# programs リストの各要素フォーマット（必須/任意）
{
    "name": "表示名",                 # 必須: str（ハブ表示・ログ用）
    "module": run,                   # 必須: モジュールオブジェクト（例: run, my_actions）
    "description": "説明文",         # 必須: str（ターミナル表示）
    "function": "関数名",             # 必須: str（module 内に存在する関数名）
    "params": [robot, hub, 100, 50], # 任意: list（関数に渡す引数。順序は関数定義に合わせる）
}
```

- **必須キー**: `name`, `module`, `description`, `function`
  - `description` は `selecter.py` の出力で必ず参照されるため省略不可
- **任意キー**: `params`
  - 省略した場合は、引数なしで関数が呼ばれます
  - 多くの関数は `robot` や `hub` を必要とするため、通常は指定します

例1: 引数あり

```python
{"name": "直進(100mm,50%)", "module": run, "description": "直進テスト", "function": "straight_with_power", "params": [robot, 100, 50]}
```

例2: 引数なし（関数側が引数不要な場合）

```python
{"name": "初期化のみ", "module": run, "description": "引数なし関数の例", "function": "init_only"}
```
#### 2.7 登録される側のプログラムの書き方

セレクターに登録する関数は「通常の同期関数」を想定しています。以下の指針に従って作成してください。

- **同期関数で書く**: `def ...`（`async def`は不可）
- **初期化はしない**: `initialize_robot()` を呼ばず、`robot` や `hub` は引数で受け取る
- **戻り値は不要**: `None` でOK
- **例外処理**: 上位で捕捉されるため、そのまま例外を投げてもOK（安全停止が必要なら関数内で `robot.stop()` などを実施）

推奨シグネチャ（例）

```python
# my_actions_gemini_2_5_pro.py
from pybricks.tools import wait

def go_and_turn(robot, hub, distance_mm: int, angle_deg: int, power: int) -> None:
    """指定距離直進→指定角度回転"""
    robot.settings(straight_speed=abs(power) * 5)
    robot.straight(distance_mm)
    wait(100)
    robot.settings(turn_rate=abs(power) * 5)
    robot.turn(angle_deg)
    hub.imu.reset_heading(0)
```

モーター等の追加デバイスが必要な場合は、引数として受け取ってください。

```python
from pybricks.pupdevices import Motor

def lift_and_move(robot, lift_motor: Motor, up_deg: int, distance_mm: int, power: int) -> None:
    lift_motor.run_target(speed=200, target_angle=up_deg)
    robot.settings(straight_speed=abs(power) * 5)
    robot.straight(distance_mm)
```

登録例（`selecter.py` の `programs`）

```python
{"name": "進む→回る", "module": my_actions, "description": "直進後に回転", "function": "go_and_turn", "params": [robot, hub, 150, 90, 40]}
{"name": "持ち上げ→前進", "module": my_actions, "description": "リフト後に前進", "function": "lift_and_move", "params": [robot, lift, 90, 200, 30]}
```

注意点
- `wait()` を適宜入れて機体保護と安定動作を確保
- `selecter.py` 側で実行前後に `reset_robot()` が呼ばれる前提のため、関数内で再初期化しない
- 長時間の無限ループなどは避け、1回の呼び出しで完了する処理にまとめる


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


#### 3.2 精度テスト（straight_with_power / turn_with_power）

直進距離と回転角度の精度を測定するための簡易テストです。下記を新規ファイルとして保存して実行できます。

- 推奨ファイル名: `accuracy_test_gemini_2_5_pro.py`

```python
from pybricks.tools import wait
from setup import initialize_robot
from run import straight_with_power, turn_with_power


def straight_accuracy_test(robot, target_mm: int = 100, power: int = 50, trials: int = 5) -> None:
    """直進精度を trials 回測定して誤差を表示"""
    errors = []
    for i in range(trials):
        robot.reset()
        straight_with_power(robot, target_mm, power)
        actual = robot.distance()
        error = actual - target_mm
        errors.append(error)
        print(f"[Straight #{i+1}] target={target_mm}mm actual={actual:.1f}mm error={error:+.1f}mm")
        wait(200)

    avg_error = sum(errors) / len(errors)
    avg_abs_error = sum(abs(e) for e in errors) / len(errors)
    print(f"AVG error={avg_error:+.1f}mm, AVG |error|={avg_abs_error:.1f}mm")


def turn_accuracy_test(robot, hub, target_deg: int = 90, power: int = 30, trials: int = 5) -> None:
    """回転精度を trials 回測定して誤差を表示"""
    errors = []
    for i in range(trials):
        hub.imu.reset_heading(0)
        turn_with_power(robot, hub, target_deg, power)
        actual = hub.imu.heading()
        error = actual - target_deg
        errors.append(error)
        print(f"[Turn #{i+1}] target={target_deg}° actual={actual:.1f}° error={error:+.1f}°")
        wait(200)

    avg_error = sum(errors) / len(errors)
    avg_abs_error = sum(abs(e) for e in errors) / len(errors)
    print(f"AVG error={avg_error:+.1f}°, AVG |error|={avg_abs_error:.1f}°")


if __name__ == "__main__":
    hub, left, right, robot = initialize_robot()

    # 直進の精度テスト（例: 100mm を出力50%で5回）
    straight_accuracy_test(robot, target_mm=100, power=50, trials=5)

    # 回転の精度テスト（例: 90° を出力30%で5回）
    turn_accuracy_test(robot, hub, target_deg=90, power=30, trials=5)
```

調整のヒント
- **タイヤ/車軸のパラメータ**: `setup.py` の `setup_robot_parameters()` で `wheel_diameter`（タイヤ径）と `axle_track`（車軸間距離）を実測に合わせて調整すると直進/旋回精度が向上します。
- **PID ゲイン**: `setup.py` の `setup_pid_control()` 内の `DISTANCE_*` と `HEADING_*` を段階的に調整。
- **実行条件**: 平坦な路面・安定したバッテリー・ケーブル干渉無しで測定。
- **パワー設定**: 高すぎる出力はオーバーシュートを招く場合あり。まずは 20–50% から。



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

