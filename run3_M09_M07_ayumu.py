from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Axis, Direction ,Color
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task
from setup import initialize_robot

async def run(hub ,robot, left_wheel, right_wheel,left_lift,right_lift):
#######################################
    # ここにロボットの動作を記述してください
   await robot.straight(100)
   await robot.turn(-40)
   await robot.straight(480)
   await robot.straight(-180)
   await robot.straight(120)
   await robot.turn(-33)
   await robot.straight(-200)
   await robot.turn(33)
   await robot.straight(390)
   await wait(500)
   right_lift.run_angle(700, -500)
   await wait(1000)
   right_lift.run_angle(1000, 700)
   
   # ロボットを明示的に停止
   robot.stop()
   print("# 走行完了！")

    # === サンプル動作コード（参考例）===
    # 以下は基本的なロボット動作の例です。必要に応じてコメントアウトを解除して使用してください
    
    # 【awaitについて】
    # await = 動作が完了するまで待機（順次実行）
    # awaitなし = 動作を開始してすぐ次の処理へ（並行実行）
    # 【実装時の注意点】
    # リフト操作：連続して同じリフトを使用する場合はwaitを使用し待ち時間を挟む。waitがないと同時に動いてしまい想定した挙動にならない。
    
    # 動作速度の設定: robot.settingsで直進・回転速度を調整
    #robot.settings(straight_speed=800, turn_rate=100)  # 直進200mm/s, 回転100deg/s
    
    # 直進移動: 300mm前進（非同期実行）
    #robot.straight(500)
    #await wait(500)
    #left_lift.run_angle(200, 360)
    
    ## リフト操作: 左リフトを速度200で360度回転（非同期実行）
    #await left_lift.run_angle(200, 360)
    #
    ## 回転動作: その場で90度右回転（非同期実行）
    #await robot.turn(90)
    #
    ## 動作中の速度変更例: より高速な設定に変更
    #robot.settings(straight_speed=400, turn_rate=200)  # 高速設定
    #
    ## リフト操作: 左リフトを速度200で360度回転（同期実行・awaitなし）
    #left_lift.run_angle(200, 360)
    #
    ## カーブ移動: 半径150mmで90度カーブ（非同期実行）
    #await robot.curve(150, 90)
    #
    ## 精密動作用の低速設定例
    #robot.settings(straight_speed=100, turn_rate=50)   # 低速・高精度設定
    #await robot.straight(50)  # 精密な50mm移動
    #pass  # 何も実行しない場合の構文エラー回避
    
##########################################


# グローバル終了フラグ
stop_logging = False

async def sensor_logger_task():
    """
    センサー値を定期的にターミナルに表示する非同期タスク。
    他のタスク（ロボットの移動）と並行して実行されます。
    """
    global stop_logging
    print("--- センサーログタスク開始 ---")
    while not stop_logging: # stop_loggingフラグがTrueになるまで継続
        heading = hub.imu.heading()
        left_deg = left_wheel.angle()
        right_deg = right_wheel.angle()
        dist = robot.distance()
        print(f"LOG: dist={dist:4.0f} mm  heading={heading:4.0f}°  L={left_deg:5.0f}°  R={right_deg:5.0f}°")
        await wait(200) # 100ミリ秒待機して、他のタスクに実行を譲る
    
    print("--- センサーログタスク終了 ---")

async def main():
    global stop_logging
    await run(hub ,robot, left_wheel, right_wheel,left_lift,right_lift)
    # main()が終了したらログタスクも終了させる
    stop_logging = True
    print("--- メインタスク完了、ログタスク終了中 ---")
    await wait(500)  # ログタスクが終了するまで少し待つ

if __name__=="__main__":
    hub ,robot, left_wheel, right_wheel,left_lift,right_lift = initialize_robot()
    run_task(multitask(
        sensor_logger_task(), 
        main()
    ))