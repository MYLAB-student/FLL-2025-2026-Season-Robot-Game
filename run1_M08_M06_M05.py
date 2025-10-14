from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Axis, Direction, Color, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task, StopWatch
from setup import initialize_robot


async def run(hub ,robot, left_wheel, right_wheel,left_lift,right_lift):

#######################################
    # ここにロボットの動作を記述してください

    # M08

    # 最初の目標地点まで前進（450mm）
    print(">>> 実行: await robot.straight(450)")
    await robot.straight(450)
    
    # 右アームを下げる（速度500、角度-1100度）
    print(">>> 実行: await right_lift.run_angle(500,-1100)")
    await right_lift.run_angle(500,-1100)
    

    # M06

    # 微調整のため左に5度回転
    print(">>> 実行: await robot.turn(-5)")
    await robot.turn(-5)
    
    # さらに前進（250mm）- 目標位置に近づく
    print(">>> 実行: await robot.straight(250)")
    await robot.straight(250)
    

    # M05

    await robot.turn(-45)
    await robot.straight(30)

    # 右の車輪だけを少し動かす（180度回転、タイムアウト1.5秒）
    print(">>> 実行: right_wheel.run_angle(200, 180) [タイムアウト1.5秒]")
    right_wheel.run_angle(200, 180, wait=False)  # 非同期で回転開始
    
    # 1.5秒待機、終わらなければ強制停止
    timeout = StopWatch()
    timeout.reset()
    while timeout.time() < 1500:
        # 回転が完了したかチェック（モーターが停止しているか）
        if not right_wheel.control.done():
            await wait(10)  # 10ミリ秒ごとにチェック
        else:
            break
    
    # タイムアウトしたら強制停止
    if not right_wheel.control.done():
        print(">>> タイムアウト: 右車輪を強制停止")
        right_wheel.stop()
        

    # ホームエリアに戻る

    # 時計回りに60度回転
    print(">>> 実行: await robot.turn(45)")
    await robot.turn(60)

    # 一時的に速度を100%に変更
    robot.settings(straight_speed=500)  # 500mm/s = 100%

    # 後退して初期位置方向に戻る（700mm）- 100%スピード
    print(">>> 実行: await robot.straight(-700) [100%スピード]")
    await robot.straight(-700)
    
    # 速度を元に戻す（40%）
    robot.settings(straight_speed=200)  # 200mm/s = 40%
    
    # ロボットを明示的に停止
    robot.stop()
    print("# 走行完了！")


    # 例: ブロイントまで移動
    # await robot.straight(400)  # 400mm前進
    # await robot.turn(45)       # 45度右回転
    
    # アームでブロックを掴む
    # await left_lift.run_angle(300, 180)  # 左アーム操作
    # await right_lift.run_angle(300, 180) # 右アーム操作
    # await wait(500)                      # 0.5秒待機
    
    # ブロックを運搬
    # await robot.straight(-100)   # 100mm後退
    # await robot.turn(-90)        # 90度左回転
    # await robot.straight(600)    # 600mm前進
    
    # ブロックを配置
    # await left_lift.run_angle(300, -180)  # アームを戻す
    # await right_lift.run_angle(300, -180)
    # await wait(300)
    
    # 初期位置に戻る
    # await robot.straight(-300)
    # await robot.turn(45)



    pass  # 何も実行しない場合の構文エラー回避
    
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
    # 経過時間測定用のタイマーを開始
    logger_timer = StopWatch()
    logger_timer.reset()
    
    while not stop_logging: # stop_loggingフラグがTrueになるまで継続
        elapsed_time = logger_timer.time()
        heading = hub.imu.heading()
        left_deg = left_wheel.angle()
        right_deg = right_wheel.angle()
        dist = robot.distance()
        print(f"LOG[{elapsed_time:5.0f}ms]: dist={dist:4.0f} mm  heading={heading:4.0f}°  L={left_deg:5.0f}°  R={right_deg:5.0f}°")
        await wait(200) # 200ミリ秒待機して、他のタスクに実行を譲る
    
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