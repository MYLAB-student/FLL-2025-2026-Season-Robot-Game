from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Axis, Direction, Button, Color
from pybricks.pupdevices import Motor, ForceSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task
from setup import initialize_robot
import run
import run1
import run_sample

dev=False

# ロボットの初期化
hub ,robot, left_wheel, right_wheel,left_lift,right_lift = initialize_robot()

# プログラムリスト
programs = [

     {"name": "run1", "module": run1, "description": "run1関数", "function": "run1", },
     {"name": "run1", "module": run_sample, "description": "run1関数", "function": "run1" ,}
    # 他のプログラムをここに追加
]



# フォースセンサーの初期化
button = ForceSensor(Port.C)

print("=== プログラムセレクター ===")
print("LEFT/RIGHT: プログラム選択")
print("フォースセンサー: プログラム実行")

async def reset_robot():
    """ロボットのリソースをリセット"""
    try:
        robot.stop()
        robot.reset()
        hub.imu.reset_heading(0)
        print("ロボットリソースをリセットしました")
    except Exception as e:
        print(f"リセットエラー: {e}")
        
async def sensor_logger_task():
    """
    センサー値を定期的にターミナルに表示する非同期タスク。
    他のタスク（ロボットの移動）と並行して実行されます。
    """
    print("--- センサーログタスク開始 ---")
    while True: # プログラムが終了するまで継続的にログを出力
        heading = hub.imu.heading()
        left_deg = left_wheel.angle()
        right_deg = right_wheel.angle()
        dist = robot.distance()
        print(f"LOG: dist={dist:4.0f} mm  heading={heading:4.0f}°  L={left_deg:5.0f}°  R={right_deg:5.0f}°")
        await wait(200) # 100ミリ秒待機して、他のタスクに実行を譲る

async def selecter_task():
    program_id = 0
    max_programs = len(programs) - 1
    while True:
        # 現在のプログラムIDを表示
        current_program = programs[program_id]
        hub.display.number(program_id)


        # ボタン入力の処理
        pressed_buttons = hub.buttons.pressed()

        if Button.RIGHT in pressed_buttons:
            program_id = (program_id + 1) % (max_programs + 1)
            hub.light.on(Color.GREEN)
            await wait(100)
            hub.light.off()
            print(f"→ プログラム {program_id} に変更")

        elif Button.LEFT in pressed_buttons:
            program_id = (program_id - 1) if program_id > 0 else max_programs
            hub.light.on(Color.BLUE)
            await wait(100)
            hub.light.off()
            print(f"← プログラム {program_id} に変更")

        # フォースセンサーでプログラム実行
        if await button.force() >= 0.5:
            hub.light.on(Color.RED)
            print(f"=== プログラム {program_id} を実行中 ===")

            try:
                # 実行前にリソースをリセット
                await reset_robot()
                await wait(50)  # リセット後に少し待機

                # 選択されたプログラムを実行
                function_name = current_program['function']
                function = getattr(current_program['module'], function_name)

                # パラメータがある場合は渡す
                if 'params' in current_program:
                    await function(*current_program['params'],hub ,robot, left_wheel, right_wheel,left_lift,right_lift)
                else:
                    await function(hub ,robot, left_wheel, right_wheel,left_lift,right_lift)

                print(f"=== プログラム {program_id} 実行完了 ===")

            except Exception as e:
                print(f"エラー: {e}")
                hub.light.on(Color.RED)
                await wait(500)
                hub.light.off()
            finally:
                # 実行後にリソースをリセット
                try:
                    await reset_robot()
                    await wait(50)  # リセット後に少し待機
                except Exception as e:
                    print(f"リセットエラー: {e}")

            hub.light.off()
            print("セレクターに戻りました")

        await wait(50)  # ボタン連打防止のため少し待つ
if dev:
    run_task(multitask(
        sensor_logger_task(),         # センサー値を継続的にログに出力するタスク
        selecter_task()
    ))
else:
        run_task(multitask(
        selecter_task()
    ))