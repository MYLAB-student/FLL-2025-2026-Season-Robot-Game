"""
【プログラムセレクター】
このファイルは、ロボットで実行したいプログラムを選んで実行するための「セレクター」です。
テレビのリモコンでチャンネルを選ぶように、複数のプログラムから好きなものを選んで実行できます。

【使い方】
1. ハブの左右ボタン（LEFT/RIGHT）でプログラムを選択
2. フォースセンサーを押すと、選んだプログラムが実行されます
3. プログラム番号がハブの画面に表示されます
"""

# ===== ライブラリのインポート =====
# 以下は、LEGOロボットを動かすために必要な「道具箱」を開いています
from pybricks.hubs import PrimeHub          # ロボットの「脳みそ」となるハブを使うための道具
from pybricks.parameters import Port, Axis, Direction, Button, Color  # ポート番号、方向、ボタン、色などの設定
from pybricks.pupdevices import Motor, ForceSensor  # モーターやセンサーを使うための道具
from pybricks.robotics import DriveBase     # ロボットの移動機能を使うための道具
from pybricks.tools import wait, multitask, run_task  # 待機や複数の動作を同時に行うための道具
from setup import initialize_robot          # ロボットを初期化（準備）する関数をインポート
import run   # run.pyファイルにある関数を使えるようにする
import run1  # run1.pyファイルにある関数を使えるようにする

# ===== ロボットの初期化 =====
# ロボットを使う準備をします（モーターやセンサーの設定を行う）
hub ,robot, left_wheel, right_wheel,left_lift,right_lift = initialize_robot()

# ===== プログラムリスト =====
# ここに、実行したいプログラムを登録します
# 各プログラムは以下の情報を持っています：
#   - name: プログラムの名前（わかりやすい名前を付けてください）
#   - module: どのファイル（run、run1など）に関数があるか
#   - description: プログラムの説明（何をするプログラムか）
#   - function: 実行する関数の名前
#   - params: 関数に渡すパラメータ（引数）のリスト
programs = [
    
    {"name": "straight_with_power", "module": run, "description": "straight_with_power関数", "function": "straight_with_power", "params": [robot,100, 50]},
     {"name": "straight_with_power", "module": run, "description": "straight_with_power関数", "function": "straight_with_power", "params": [robot,100, 10]},
     {"name": "回転", "module": run, "description": "回転", "function": "turn_with_power", "params": [robot,hub,100, 10]},
     {"name": "run1", "module": run1, "description": "run1関数", "function": "run1", "params": [hub ,robot, left_wheel, right_wheel,left_lift,right_lift]},
    # 他のプログラムをここに追加できます
    # 例: {"name": "新しいプログラム", "module": run, "description": "説明", "function": "関数名", "params": [引数]},
]

# ===== プログラム選択の変数 =====
program_id = 0                      # 現在選択されているプログラムの番号（0から始まる）
max_programs = len(programs) - 1    # プログラムの総数-1（最後のプログラム番号）

# ===== フォースセンサーの初期化 =====
# ポートCに接続されたフォースセンサー（押すボタン）を使えるようにします
button = ForceSensor(Port.C)

# ===== 使い方の説明を表示 =====
print("=== プログラムセレクター ===")
print("LEFT/RIGHT: プログラム選択")
print("フォースセンサー: プログラム実行")

# ===== ロボットをリセットする関数 =====
def reset_robot():
    """
    ロボットを初期状態に戻す関数
    プログラム実行前後に呼び出されて、ロボットをクリーンな状態にします
    """
    try:
        robot.stop()                  # ロボットの動きを停止
        robot.reset()                 # ロボットの走行距離などをリセット
        hub.imu.reset_heading(0)      # ジャイロセンサー（向き）を0度にリセット
        print("ロボットリソースをリセットしました")
    except Exception as e:
        # エラーが発生した場合はメッセージを表示
        print(f"リセットエラー: {e}")

# ===== メインループ（プログラムの本体） =====
# このループは永遠に繰り返されます（電源を切るまで動き続けます）
while True:
    # ----- 現在選択中のプログラム情報を取得 -----
    current_program = programs[program_id]  # programsリストから現在のプログラムを取得
    hub.display.number(program_id)          # ハブの画面にプログラム番号を表示
    
    # ----- プログラム名をコンピューターの画面に表示 -----
    print(f"選択中: {program_id} - {current_program['name']} ({current_program['description']})")
    
    # ----- ハブのボタン入力をチェック -----
    pressed_buttons = hub.buttons.pressed()  # 押されているボタンを確認
    
    # 【右ボタンが押された場合】次のプログラムに進む
    if Button.RIGHT in pressed_buttons:
        # プログラム番号を1つ増やす（最後まで行ったら0に戻る）
        program_id = (program_id + 1) % (max_programs + 1)
        hub.light.on(Color.GREEN)    # ハブのライトを緑色に点灯
        wait(100)                     # 0.1秒待つ
        hub.light.off()               # ライトを消す
        print(f"→ プログラム {program_id} に変更")
        
    # 【左ボタンが押された場合】前のプログラムに戻る
    elif Button.LEFT in pressed_buttons:
        # プログラム番号を1つ減らす（0より前に行ったら最後に戻る）
        program_id = (program_id - 1) if program_id > 0 else max_programs
        hub.light.on(Color.BLUE)     # ハブのライトを青色に点灯
        wait(100)                     # 0.1秒待つ
        hub.light.off()               # ライトを消す
        print(f"← プログラム {program_id} に変更")
    
    # ----- フォースセンサーでプログラム実行 -----
    # フォースセンサーが0.5以上の力で押されたら、プログラムを実行
    if button.force() >= 0.5:
        hub.light.on(Color.RED)       # ハブのライトを赤色に点灯（実行中を示す）
        print(f"=== プログラム {program_id} を実行中 ===")
        
        try:
            # ----- 実行前の準備 -----
            reset_robot()             # ロボットをリセットして、前のプログラムの影響をなくす
            wait(50)                  # リセット後に少し待機（0.05秒）
            
            # ----- プログラムを実行 -----
            # 選択されたプログラムの関数名を取得
            function_name = current_program['function']
            # モジュールから関数を取得（例: run.pyのstraight_with_power関数）
            function = getattr(current_program['module'], function_name)
            
            # パラメータ（引数）がある場合は渡して実行、ない場合はそのまま実行
            if 'params' in current_program:
                function(*current_program['params'])  # *は「リストの中身を展開して渡す」という意味
            else:
                function()  # パラメータなしで実行
                
            print(f"=== プログラム {program_id} 実行完了 ===")
            
        except Exception as e:
            # ----- エラーが発生した場合の処理 -----
            print(f"エラー: {e}")     # エラーメッセージを表示
            hub.light.on(Color.RED)   # 赤いライトを点灯してエラーを知らせる
            wait(500)                 # 0.5秒待つ
            hub.light.off()           # ライトを消す
        finally:
            # ----- 実行後の後処理（必ず実行される） -----
            # finallyブロックは、エラーがあってもなくても必ず実行されます
            try:
                reset_robot()         # 実行後にロボットをリセット
                wait(50)              # リセット後に少し待機（0.05秒）
            except Exception as e:
                print(f"リセットエラー: {e}")
        
        hub.light.off()               # ライトを消す
        print("セレクターに戻りました")
    
    # ----- ボタン連打防止のための待機 -----
    # 少し待つことで、ボタンを何度も押してしまうのを防ぎます
    wait(50)  # 0.05秒待つ
