from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Axis, Direction ,Color
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task
from setup import initialize_robot

async def run(hub ,robot, left_wheel, right_wheel,left_lift,right_lift):
#######################################
    # ここにロボットの動作を記述してください
    # === サンプル動作コード（参考例）===
    # 以下は基本的なロボット動作の例です。必要に応じてコメントアウトを解除して使用してください
    
    # 【awaitについて】
    # await = 動作が完了するまで待機（順次実行）
    # awaitなし = 動作を開始してすぐ次の処理へ（並行実行）
    
    # 動作速度の設定: robot.settingsで直進・回転速度を調整
    robot.settings(straight_speed=400, turn_rate=240)  # 直進200mm/s, 回転100deg/s
    
    # 直進移動: 300mm前進（非同期実行）

    await robot.straight(450)
    await right_lift.run_angle(500, -360)
    await wait(100)
    await right_lift.run_angle(500, -360)
    await wait(100)
    await right_lift.run_angle(500, -360)
    await wait(100)


    await robot.straight(240)


    await robot.turn(-50)


    await robot.straight(80)


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
    pass  # 何も実行しない場合の構文エラー回避
    
##########################################


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

async def main():
    await run(hub ,robot, left_wheel, right_wheel,left_lift,right_lift)

if __name__=="__main__":
    hub ,robot, left_wheel, right_wheel,left_lift,right_lift = initialize_robot()
    run_task(multitask(
        sensor_logger_task(), 
        main()
    ))