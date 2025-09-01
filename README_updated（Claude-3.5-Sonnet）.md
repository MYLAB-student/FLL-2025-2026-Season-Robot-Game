# LEGO SPIKE Prime ロボット制御プログラム（Claude-3.5-Sonnet）

このプロジェクトは、LEGO SPIKE PrimeロボットをPybricksを使用して制御するためのPythonプログラム群です。

## 📑 目次

- [📁 プロジェクト構成](#-プロジェクト構成)
- [⚡ 開発時の流れ](#-開発時の流れ)
  - [新しいミッションファイルの作成方法（run_template.py使用）](#新しいミッションファイルの作成方法run_templatepy使用)
  - [新しいランファイルの作成手順](#新しいランファイルの作成手順)
  - [ローバー・アーム操作の詳細例](#ローバーアーム操作の詳細例)
    - [🚗 単純な操作](#-単純な操作)
    - [🔄 複雑な操作](#-複雑な操作)
    - [🎯 実践的なミッション例](#-実践的なミッション例)
    - [💡 モーター制御のコツ](#-モーター制御のコツ)
  - [selector.pyでの登録手順](#selectorpyでの登録手順)
- [⚡ 競技時の操作方法](#-競技時の操作方法)
- [🚀 機能](#-機能)
- [🔧 セットアップ](#-セットアップ)
- [📖 使用方法](#-使用方法)
- [⚙️ 設定パラメータ](#️-設定パラメータ)
- [🔍 センサー情報](#-センサー情報)
  - [ログ機能のオン・オフ切り替え](#ログ機能のオンオフ切り替え)
- [🛠️ カスタマイズ](#️-カスタマイズ)
- [⚠️ 注意事項](#️-注意事項)
- [🐛 トラブルシューティング](#-トラブルシューティング)

## 📁 プロジェクト構成

```
FLL-2025-2026-Season/
├── README.md              # このファイル
├── selecter.py           # プログラム選択・実行インターフェース（競技用）
├── selecter_dev.py       # プログラム選択・実行インターフェース（開発用・ログ機能付き）
├── setup.py              # ロボット初期化モジュール
├── run_template.py       # 新しいミッションファイル作成用テンプレート
├── run.py                # 基本動作関数集
├── run1.py               # ミッション実行ファイル例
├── run_sample.py         # サンプルミッション
└── straight_test.py      # 直進・回転テスト用プログラム
```

## ⚡ 開発時の流れ

### 新しいミッションファイルの作成方法（run_template.py使用）

このプロジェクトでは、`run_template.py`を使って新しいミッションファイルを効率的に作成できます。

#### 1. run_template.pyの概要

`run_template.py`は新しいミッションファイル作成のためのテンプレートファイルです。

**特徴:**
- 基本的なロボット動作のサンプルコード（コメントアウト済み）
- 詳細なコメント付きで動作の理解がしやすい
- センサーログ機能付き
- 非同期処理対応
- そのまま実行可能

**基本構造:**
```python
# run_template.py
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Axis, Direction ,Color
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task
from setup import initialize_robot

async def run(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    # ここにロボットの動作を記述してください
    # === サンプル動作コード（参考例）===
    # 以下は基本的なロボット動作の例です。必要に応じてコメントアウトを解除して使用してください
    
    # リフト操作: 左リフトを速度200で360度回転（非同期実行）
    # await left_lift.run_angle(200, 360)
    
    # 直進移動: 300mm前進（非同期実行）
    # await robot.straight(300)
    
    # 回転動作: その場で90度右回転（非同期実行）
    # await robot.turn(90)
    
    # リフト操作: 左リフトを速度200で360度回転（同期実行・awaitなし）
    # left_lift.run_angle(200, 360)
    
    # カーブ移動: 半径150mmで90度カーブ（非同期実行）
    # 注意: robot.arc()は廃止されました。robot.curve()を使用してください
    # await robot.curve(150, 90)
    pass  # 何も実行しない場合の構文エラー回避

# センサーログ機能とメイン実行機能を含む
```

#### 2. 新しいミッションファイルの作成手順

1. **ファイルのコピー**
   ```bash
   # run_template.pyをコピーして新しいミッションファイルを作成
   cp run_template.py mission01（Claude-3.5-Sonnet）.py
   ```

2. **run関数の編集**
   ```python
   # mission01（Claude-3.5-Sonnet）.py
   async def run(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
       """ミッション1: ブロック運搬"""
       # ここにミッション固有の動作を記述
       
       # 例: ブロック取得ポイントまで移動
       await robot.straight(400)  # 400mm前進
       await robot.turn(45)       # 45度右回転
       
       # アームでブロックを掴む
       await left_lift.run_angle(300, 180)  # 左アーム操作
       await right_lift.run_angle(300, 180) # 右アーム操作
       await wait(500)                      # 0.5秒待機
       
       # ブロックを運搬
       await robot.straight(-100)   # 100mm後退
       await robot.turn(-90)        # 90度左回転
       await robot.straight(600)    # 600mm前進
       
       # ブロックを配置
       await left_lift.run_angle(300, -180)  # アームを戻す
       await right_lift.run_angle(300, -180)
       await wait(300)
       
       # 初期位置に戻る
       await robot.straight(-300)
       await robot.turn(45)
   ```

3. **単体テスト実行**
   ```bash
   # 新しいミッションファイルを直接実行してテスト
   python mission01（Claude-3.5-Sonnet）.py
   ```

#### 3. selecter_dev.pyへの登録

1. **インポート文の追加**
   ```python
   # selecter_dev.py の先頭付近に追加
   import run
   import run1
   import run_sample
   import mission01_claude_3_5_sonnet as mission01  # 新しく追加（括弧は使えないため）
   ```

2. **programsリストへの追加**
   ```python
   # selecter_dev.py のprogramsリストに新しいエントリを追加
   programs = [
       {"name": "straight_with_power", "module": run, "description": "straight_with_power関数", "function": "straight_with_power", "params": [robot,100, 50]},
       {"name": "straight_with_power", "module": run, "description": "straight_with_power関数", "function": "straight_with_power", "params": [robot,100, 10]},
       {"name": "回転", "module": run, "description": "回転", "function": "turn_with_power", "params": [robot,hub,100, 10]},
       {"name": "run1", "module": run1, "description": "run1関数", "function": "run1", "params": [hub ,robot, left_wheel, right_wheel,left_lift,right_lift]},
       {"name": "run1", "module": run_sample, "description": "run1関数", "function": "run1", "params": [hub ,robot, left_wheel, right_wheel,left_lift,right_lift]},
       {"name": "ミッション1", "module": mission01, "description": "ブロック運搬ミッション", "function": "run", "params": [hub ,robot, left_wheel, right_wheel,left_lift,right_lift]},  # 新しく追加
       # 他のプログラムをここに追加
   ]
   ```

#### 4. selecter_dev.pyでのテスト実行

1. **開発モードでの実行**
   ```bash
   # selecter_dev.py を実行（センサーログ有効）
   python selecter_dev.py
   ```

2. **操作方法**
   - **LEFTボタン**: 前のプログラムに切り替え
   - **RIGHTボタン**: 次のプログラムに切り替え  
   - **フォースセンサー**: 選択したプログラムを実行

3. **デバッグ機能**
   ```python
   # selecter_dev.py の11行目でログの有効/無効を切り替え
   dev = True   # センサーログ表示
   dev = False  # センサーログ非表示（高速実行）
   ```

#### 5. ファイル命名規則

**推奨ファイル名:**
- `mission01（Claude-3.5-Sonnet）.py` ← ユーザールール対応
- `task_delivery（Claude-3.5-Sonnet）.py`
- `bridge_mission（Claude-3.5-Sonnet）.py`

**インポート時の注意:**
```python
# 括弧やハイフンを含むファイル名は通常のインポートができない
# import mission01（Claude-3.5-Sonnet）  # エラー

# 解決方法1: ファイル名を変更
# mission01_claude_3_5_sonnet.py にリネーム
import mission01_claude_3_5_sonnet as mission01

# 解決方法2: importlibを使用（括弧付きファイル名の場合）
import importlib.util, sys
spec = importlib.util.spec_from_file_location("mission01", "mission01（Claude-3.5-Sonnet）.py")
mission01 = importlib.util.module_from_spec(spec)
sys.modules["mission01"] = mission01
spec.loader.exec_module(mission01)
```

#### 6. 運用フロー

```
1. run_template.py をコピー
     ↓
2. ミッション内容に合わせて run関数 を編集
     ↓
3. 単体で動作テスト（python mission●.py）
     ↓
4. selecter_dev.py にインポート・登録
     ↓
5. セレクターでの動作確認（dev=True）
     ↓
6. 問題なければ selecter.py にも登録
     ↓
7. 競技用として selecter.py をハブに書き込み
```

#### 7. run_template.pyとselecter_dev.pyの連携メリット

- **効率的な開発**: テンプレートで基本構造を素早く作成
- **統一された形式**: 全てのミッションファイルが同じ構造
- **デバッグ支援**: selecter_dev.pyのセンサーログで動作確認
- **段階的テスト**: 単体テスト → セレクター統合テスト
- **簡単な切り替え**: ボタン操作で複数ミッションを素早く実行

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

### ローバー・アーム操作の詳細例

このプロジェクトでは、**ローバー用2つのモーター**と**アーム用2つのモーター**の計4つのモーターを制御できます。以下に具体的な操作パターンの記載例を示します。

#### 🚗 単純な操作

##### ローバーを動かす（robot, left_wheel, right_wheel使用）

**基本的な移動:**
```python
def basic_movement_example(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """基本的なローバー移動の例"""
    # 前進
    robot.straight(300)  # 300mm前進
    wait(200)
    
    # 後進
    robot.straight(-200)  # 200mm後進
    wait(200)
    
    # 回転（その場回転）
    robot.turn(90)   # 90度右回転
    wait(200)
    robot.turn(-90)  # 90度左回転
    wait(200)
```

**前進しながら曲がる（カーブ移動）:**
```python
def curve_movement_example(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """カーブ移動の例"""
    # 大きな弧を描いて移動（radius: 半径, angle: 角度）
    robot.curve(200, 90)   # 半径200mmで90度カーブ
    wait(300)
    
    # 逆方向のカーブ
    robot.curve(150, -45)  # 半径150mmで45度左カーブ
    wait(300)
```

**その場での向き変更（2つの方法）:**
```python
def rotation_methods_example(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """回転方法の比較例"""
    # 方法1: 両輪逆回転（高速・正確）
    robot.turn(180)  # robotオブジェクトを使用
    wait(500)
    
    # 方法2: 片輪のみ回転（ゆっくり・安定）
    left_wheel.run_angle(200, 360)   # 左輪のみ360度回転
    wait(500)
    
    # 方法3: 手動で両輪制御（細かい調整可能）
    left_wheel.run_angle(300, 180, wait=False)   # 左輪正転（非同期）
    right_wheel.run_angle(300, -180)             # 右輪逆転（同期）
    wait(200)
```

##### アーム用モーターを動かす（left_lift, right_lift使用）

**単純なアーム操作:**
```python
def simple_arm_example(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """基本的なアーム操作の例"""
    # 両アームを同時に上げる
    left_lift.run_angle(500, 180)   # 速度500で180度回転
    right_lift.run_angle(500, 180)
    wait(300)
    
    # 両アームを同時に下げる
    left_lift.run_angle(500, -180)
    right_lift.run_angle(500, -180)
    wait(300)
    
    # 片方のアームのみ操作
    left_lift.run_angle(300, 90)    # 左アームのみ90度回転
    wait(200)
    left_lift.run_angle(300, -90)   # 元の位置に戻す
    wait(200)
```

#### 🔄 複雑な操作

##### ローバー移動後にアーム操作（順次実行）

```python
def sequential_operation_example(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """順次操作の例: 移動→停止→アーム操作"""
    # ステップ1: 目標地点まで移動
    robot.straight(400)     # 400mm前進
    robot.turn(45)          # 45度回転
    robot.straight(200)     # さらに200mm前進
    
    # ステップ2: 完全停止を確認
    robot.stop()
    wait(500)               # 振動が収まるまで待機
    
    # ステップ3: アーム操作開始
    print("アーム操作開始")
    left_lift.run_angle(400, 270)   # 左アーム270度回転
    right_lift.run_angle(400, 270)  # 右アーム270度回転
    wait(1000)                      # アーム動作完了待ち
    
    # ステップ4: アームを戻して移動再開
    left_lift.run_angle(400, -270)
    right_lift.run_angle(400, -270)
    wait(500)
    robot.straight(-200)            # 後退
```

##### ローバー移動中にアーム操作（並行実行）

```python
def parallel_operation_example(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """並行操作の例: 移動しながらアーム操作"""
    # 移動開始と同時にアーム操作開始（非同期）
    left_lift.run_angle(300, 180, wait=False)   # wait=Falseで非同期実行
    right_lift.run_angle(300, 180, wait=False)
    
    # アームが動いている間にローバーも移動
    robot.straight(500)     # アーム動作中に移動
    wait(200)               # アーム動作完了を待つ
    
    # 移動しながらアームを戻す
    left_lift.run_angle(400, -180, wait=False)
    right_lift.run_angle(400, -180, wait=False)
    robot.turn(90)          # アームが戻りながら回転
    wait(500)
```

##### 片方のアーム動作中にもう片方のアーム操作

```python
def independent_arm_example(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """独立したアーム操作の例"""
    # 左アームを動かし始める（非同期）
    left_lift.run_angle(200, 360, wait=False)
    wait(500)               # 少し遅れて...
    
    # 右アームも動かし始める（非同期）
    right_lift.run_angle(300, -180, wait=False)
    wait(200)
    
    # 両方のアームが動いている間にローバーも移動
    robot.straight(300)
    
    # 左アームの動作が終わったら別の動作
    wait(1000)              # 左アーム完了を待つ
    left_lift.run_angle(400, -180)  # 左アームを逆方向に
    
    # 右アームはまだ動いている可能性があるので待つ
    wait(800)               # 右アーム完了を待つ
    right_lift.run_angle(400, 90)   # 右アームの追加動作
```

#### 🎯 実践的なミッション例

```python
def mission_complete_example(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """実際のミッションを想定した複合操作"""
    print("ミッション開始: ブロック取得・運搬・配置")
    
    # フェーズ1: ブロック取得地点まで移動
    robot.straight(600)
    robot.turn(45)
    robot.straight(300)
    
    # フェーズ2: ブロック取得（アーム操作）
    print("ブロック取得中...")
    left_lift.run_angle(300, 90, wait=False)   # 両アーム展開
    right_lift.run_angle(300, 90, wait=False)
    robot.straight(100)                        # ブロックに接近
    wait(500)
    left_lift.run_angle(300, -120)             # ブロックを掴む
    right_lift.run_angle(300, -120)
    wait(300)
    
    # フェーズ3: 運搬（移動中にアーム保持）
    print("運搬中...")
    robot.straight(-100)                       # ブロックから離れる
    robot.turn(-90)                           # 配置地点へ向く
    
    # 運搬中にアームの位置調整
    left_lift.run_angle(200, 30, wait=False)  # 運搬しやすい位置に
    right_lift.run_angle(200, 30, wait=False)
    robot.straight(800)                        # 配置地点まで移動
    
    # フェーズ4: ブロック配置
    print("ブロック配置中...")
    robot.straight(50)                         # 配置位置に精密接近
    left_lift.run_angle(400, 120)             # ブロックを配置
    right_lift.run_angle(400, 120)
    wait(500)
    robot.straight(-150)                       # 配置地点から離脱
    
    # フェーズ5: 初期位置に戻る
    left_lift.run_angle(500, -90)             # アームを初期位置に
    right_lift.run_angle(500, -90)
    robot.turn(180)                           # 向きを戻す
    robot.straight(600)                        # 初期位置まで移動
    
    print("ミッション完了!")
```

#### 💡 モーター制御のコツ

**速度設定の目安:**
- 精密作業: 100-300
- 通常動作: 300-500  
- 高速移動: 500-800

**wait()の使い方:**
- 機械的な動作後: `wait(200-500)`
- 振動収束待ち: `wait(300-800)`
- 安全確認: `wait(100-200)`

**非同期実行(`wait=False`)の活用:**
- 複数モーターの同時動作
- 移動とアーム操作の並行実行
- 効率的な時間短縮

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
       {"name": "run1", "module": run1, "description": "run1関数", "function": "run1", "params": [hub, robot, left_wheel, right_wheel, left_lift, right_lift]},
       {"name": "run2", "module": run2, "description": "run2関数", "function": "run2", "params": [hub, robot, left_wheel, right_wheel, left_lift, right_lift]},  # 新しく追加
       # 他のプログラムをここに追加
   ]
   ```

3. **プログラムエントリの構成要素**

   各プログラムエントリは辞書形式で以下の要素を含みます：

   **必須要素:**
   - `name`: セレクター表示名（短くわかりやすく）
   - `module`: インポートしたモジュール名
   - `description`: 詳細説明（ターミナル表示用）
   - `function`: 実行する関数名（文字列）

   **任意要素:**
   - `params`: 関数に渡すパラメータのリスト（省略時は引数なしで実行）

   **具体例:**

   ```python
   # 例1: 基本的なrun関数の登録
   {
       "name": "run2",                    # ハブディスプレイに表示される名前
       "module": run2,                    # インポートしたrun2モジュール
       "description": "ミッション2実行",   # ターミナルに表示される詳細説明
       "function": "run2",                # run2モジュール内のrun2関数を実行
       "params": [hub, robot, left_wheel, right_wheel, left_lift, right_lift]  # 関数に渡す引数
   }

   # 例2: runモジュールの関数を使用
   {
       "name": "直進テスト",
       "module": run,
       "description": "100mm直進（50%パワー）",
       "function": "straight_with_power",
       "params": [robot, 100, 50]         # robot, 距離, パワーの順
   }

   # 例3: 回転動作
   {
       "name": "右90度",
       "module": run,
       "description": "90度右回転（30%パワー）",
       "function": "turn_with_power",
       "params": [robot, hub, 90, 30]     # robot, hub, 角度, パワーの順
   }

   # 例4: パラメータなしの関数（引数が不要な場合）
   {
       "name": "初期化",
       "module": setup_module,
       "description": "ロボット初期化のみ",
       "function": "reset_all"
       # paramsを省略 = 引数なしで実行
   }
   ```

   **パラメータ設定のコツ:**
   - `params`の順序は関数定義の引数順序と完全に一致させる
   - ロボットオブジェクト（hub, robot等）は最初に配置することが多い
   - 数値パラメータ（距離、角度、パワー等）は後に配置
   - 省略した場合は引数なしで関数が呼ばれる

   **よくある間違いと対策:**
   ```python
   # ❌ 間違い: 引数の順序が関数定義と異なる
   {"function": "straight_with_power", "params": [100, robot, 50]}  # robot が2番目になっている

   # ✅ 正しい: 関数定義 def straight_with_power(robot, distance_mm, motor_power) に合わせる
   {"function": "straight_with_power", "params": [robot, 100, 50]}

   # ❌ 間違い: 必要な引数が不足
   {"function": "run2", "params": [robot, hub]}  # left_wheel, right_wheel, left_lift, right_lift が不足

   # ✅ 正しい: 関数が要求するすべての引数を提供
   {"function": "run2", "params": [hub, robot, left_wheel, right_wheel, left_lift, right_lift]}
   ```

4. **動作確認**
   - selecter.pyを実行してプログラムリストに表示されることを確認
   - ハブのボタンで選択し、フォースセンサーで実行テスト

5. **ハブへの書き込み**
   - Pybricks Appからselecter.pyをメインとしてハブにダウンロード
   - オフライン実行が可能になる

### 注意点とベストプラクティス

#### runファイルの関数引数について

**重要**: runファイルの関数は、selecter.pyで初期化されたロボットオブジェクトを受け取る形式にする必要があります。

**関数シグネチャの標準形式**:
```python
def run●(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """
    Args:
        hub: PrimeHubオブジェクト（ジャイロセンサー、ボタン、ディスプレイ等）
        robot: DriveBaseオブジェクト（直進・回転制御）
        left_wheel: 左車輪モーターオブジェクト
        right_wheel: 右車輪モーターオブジェクト  
        left_lift: 左リフトモーターオブジェクト
        right_lift: 右リフトモーターオブジェクト
    """
    # ミッション動作をここに記述
```

**具体例 1: 基本的な移動とリフト操作**
```python
def run2(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """ミッション2: 前進してブロックを持ち上げる"""
    # 200mm前進
    robot.straight(200)
    
    # リフトを上げる（360度回転）
    left_lift.run_angle(360, 360)
    right_lift.run_angle(360, 360)
    
    # 少し待機
    wait(500)
    
    # 100mm後退
    robot.straight(-100)
    
    # ジャイロセンサーをリセット
    hub.imu.reset_heading(0)
```

**具体例 2: 複雑なルート移動**
```python
def run3(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    """ミッション3: L字ルート移動"""
    # 最初の直進
    robot.straight(300)
    
    # 90度右回転
    robot.turn(90)
    
    # リフトで何かを掴む動作
    left_lift.run_angle(500, 180)   # ゆっくり180度
    right_lift.run_angle(500, 180)
    
    # 2番目の直進
    robot.straight(200)
    
    # リフトを戻す
    left_lift.run_angle(500, -180)
    right_lift.run_angle(500, -180)
    
    # 最終位置調整
    robot.turn(-45)
    robot.straight(100)
```

**selecter.pyでの対応する登録例**:
```python
programs = [
    # 既存のエントリ...
    {"name": "run2", "module": run2, "description": "ミッション2: ブロック持ち上げ", "function": "run2", "params": [hub, robot, left_wheel, right_wheel, left_lift, right_lift]},
    {"name": "run3", "module": run3, "description": "ミッション3: L字ルート", "function": "run3", "params": [hub, robot, left_wheel, right_wheel, left_lift, right_lift]},
]
```

#### その他の注意点
- インポート順序はselecter.pyで参照する順番に合わせる
- プログラム名は重複しないよう注意する
- 関数内で`wait()`を適宜使用してロボットの安定動作を確保する
- エラーが発生しやすい動作の前後には`robot.stop()`を入れることを推奨



### ⚡ 競技時の操作方法

1) ハードウェア接続
- Port F: 左ホイールモーター（反時計回り）
- Port B: 右ホイールモーター（時計回り）
- Port E: 左リフトモーター（時計回り）
- Port A: 右リフトモーター（時計回り）
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
- 例: `missions_claude_3_5_sonnet.py`を作成

```python
# missions_claude_3_5_sonnet.py
from pybricks.tools import wait

def m01_bridge(robot, hub):
    #ここに処理を書く
    robot.settings()
    robot.straight(200)
    wait(200)
```

- `selecter.py` にインポートして登録

```python
import missions_claude_3_5_sonnet

programs += [
    {"name": "M01 ブリッジ", "module": missions_claude_3_5_sonnet, "description": "M01: 橋アプローチ", "function": "m01_bridge", "params": [robot, hub]},
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
- 4つのモーター（Port F, Port B, Port E, Port A）
- フォースセンサー（Port C、オプション）

### ハードウェア設定
```
Port F: 左ホイールモーター（反時計回り）
Port B: 右ホイールモーター（時計回り）
Port E: 左リフトモーター（時計回り）
Port A: 右リフトモーター（時計回り）
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
hub, robot, left_wheel, right_wheel, left_lift, right_lift = initialize_robot()

# カスタム設定で初期化
hub, robot, left_wheel, right_wheel, left_lift, right_lift = initialize_robot(
    straight_speed_percent=50,    # 直進速度50%
    turn_speed_percent=40,        # 旋回速度40%
    motor_power_percent=80        # モーターパワー80%
)
```



### 2. プログラム選択モード

#### 2.1 セレクターの起動
```bash
# selecter.pyを実行（競技用）
python selecter.py

# selecter_dev.pyを実行（開発用・ログ付き）
python selecter_dev.py
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
  - 例: `my_actions_claude_3_5_sonnet.py`（括弧やハイフンは使わない）

1) 新しいファイルを作成（例: `my_actions_claude_3_5_sonnet.py`）

```python
"""Generated with Claude-3.5-Sonnet"""

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
import my_actions_claude_3_5_sonnet as my_actions
```

補足: ファイル名にモデル名を括弧付きで含めたい場合

- 例: `my_actions（Claude-3.5-Sonnet）.py` のように括弧やハイフンを含むと、`import my_actions（...）` のような通常のインポートはできません。
- この場合は `importlib` を使ってファイルパスから読み込みます（下記例ではモジュール名を `my_actions` に割り当て）。

```python
import importlib.util, sys

module_path = "my_actions（Claude-3.5-Sonnet）.py"
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
# my_actions_claude_3_5_sonnet.py
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
{"name": "持ち上げ→前進", "module": my_actions, "description": "リフト後に前進", "function": "lift_and_move", "params": [robot, left_lift, 90, 200, 30]}
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

- 推奨ファイル名: `accuracy_test_claude_3_5_sonnet.py`

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
    hub, robot, left_wheel, right_wheel, left_lift, right_lift = initialize_robot()

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
    print(f"左モーター角度: {left_wheel.angle()}°")
    print(f"右モーター角度: {right_wheel.angle()}°")
    print(f"左リフト角度: {left_lift.angle()}°")
    print(f"右リフト角度: {right_lift.angle()}°")
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
        hub, robot, left_wheel, right_wheel, left_lift, right_lift = initialize_robot()
        
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

### ログ機能のオン・オフ切り替え

プロジェクトには開発用と競技用でログ機能を切り替えられる仕組みが実装されています。

#### ファイル別のログ機能

| ファイル | ログ機能 | 用途 |
|---------|---------|------|
| `selecter.py` | **なし** | 競技本番用（高速実行） |
| `selecter_dev.py` | **切り替え可能** | 開発・デバッグ用 |
| `straight_test.py` | **常時有効** | テスト・調整用 |

#### selecter_dev.pyでのログ切り替え

**ログ有効にする場合:**
```python
# selecter_dev.py の11行目を編集
dev = True  # ログを表示

# 実行時の動作
run_task(multitask(
    sensor_logger_task(),  # センサーログタスクを並行実行
    selecter_task()        # プログラム選択タスク
))
```

**ログ無効にする場合:**
```python
# selecter_dev.py の11行目を編集
dev = False  # ログを非表示

# 実行時の動作
run_task(multitask(
    selecter_task()        # プログラム選択タスクのみ実行
))
```

#### ログ表示の詳細

**更新間隔:** 200ms（0.2秒）ごと  
**表示フォーマット:**
```
--- センサーログタスク開始 ---
LOG: dist= 150 mm  heading=  45°  L=  180°  R=  180°
LOG: dist= 165 mm  heading=  47°  L=  195°  R=  195°
LOG: dist= 180 mm  heading=  48°  L=  210°  R=  210°
```

#### 使用場面別の推奨設定

**🔧 開発・デバッグ時:**
- `selecter_dev.py`を使用
- `dev = True`に設定
- センサー値をリアルタイムで確認しながら調整

**🏁 競技本番時:**
- `selecter.py`を使用
- ログオーバーヘッドなしで最高性能を発揮

**🧪 精度テスト時:**
- `straight_test.py`を使用
- 常時ログ有効で詳細な動作確認

#### パフォーマンスへの影響

| 設定 | CPU使用率 | メモリ使用量 | 応答性 |
|------|-----------|-------------|---------|
| ログ有効 | 高 | 中 | やや低下 |
| ログ無効 | 低 | 低 | 最高 |

**注意点:**
- ログが有効な場合、200msごとのprint処理により若干の性能低下があります
- 競技時はログを無効にすることで最高のパフォーマンスを確保できます
- 開発時はログを有効にしてロボットの状態を把握することが重要です

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
5. **API変更**: `robot.arc()`は廃止されました。`robot.curve()`を使用してください

## 🐛 トラブルシューティング

### よくある問題
- **直進精度が悪い**: PIDパラメータの調整が必要
- **モーターが逆回転**: `positive_direction`の設定を確認
- **センサー値が異常**: ジャイロセンサーのリセットを実行
- **Device or resource busy**: 他のプログラムがモーターを使用中。ロボットを再起動

### デバッグ方法
1. センサーログを確認（`selecter_dev.py`で`dev = True`）
2. 各ステップで`print()`文を追加
3. エラーメッセージを確認
4. `robot.stop()`と`robot.reset()`でリソースをクリア

### パフォーマンス最適化
- 競技時は`selecter.py`（ログなし）を使用
- 不要な`wait()`を削除
- 並行処理（`wait=False`）の活用
- PID設定の最適化

