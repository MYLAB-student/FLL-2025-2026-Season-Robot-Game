from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Axis, Direction, Color, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task, StopWatch
from setup import initialize_robot


async def run(hub ,robot, left_wheel, right_wheel,left_lift,right_lift):
#######################################
    # ここにロボットの動作を記述してください
    
    # ステップ1: 目標地点に向かって前進
    await robot.straight(350)  # 350mm直進して移動
    
    # ステップ2: 位置調整のため少し後退
    await robot.straight(-130)  # 130mm後退して最適な位置に調整
    
    # ステップ3: カーブしながら前進（タイムアウト処理付き）
    # カーブ動作を開始（非同期）
    robot.curve(850, 10, then=Stop.COAST, wait=False)  # カーブ動作を非同期で開始
    
    # タイムアウト処理: 3秒以内に完了しなければ強制終了
    timeout = StopWatch()  # タイマーを作成
    timeout.reset()  # タイマーをリセット
    while timeout.time() < 3000:  # 3000ミリ秒（3秒）までループ
        # カーブ動作が完了したかチェック
        if not robot.done():
            await wait(10)  # まだ動作中の場合、10ミリ秒待機してから再チェック
        else:
            break  # 動作完了したらループを抜ける
    
    robot.stop()  # タイムアウトまたは完了後に停止
    
    # ステップ4: スタート地点に向けて後退
    await robot.straight(-450)  # 450mm後退してベースに戻る 

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



async def sensor_logger_task():
    """
    センサー値を定期的にターミナルに表示する非同期タスク。
    他のタスク（ロボットの移動）と並行して実行されます。
    """
    print("--- センサーログタスク開始 ---")
    # 経過時間測定用のタイマーを開始
    logger_timer = StopWatch()
    logger_timer.reset()
    
    while True: # プログラムが終了するまで継続的にログを出力
        elapsed_time = logger_timer.time()
        heading = hub.imu.heading()
        left_deg = left_wheel.angle()
        right_deg = right_wheel.angle()
        dist = robot.distance()
        print(f"LOG[{elapsed_time:5.0f}ms]: dist={dist:4.0f} mm  heading={heading:4.0f}°  L={left_deg:5.0f}°  R={right_deg:5.0f}°")
        await wait(200) # 200ミリ秒待機して、他のタスクに実行を譲る

async def main():
    await run(hub ,robot, left_wheel, right_wheel,left_lift,right_lift)

if __name__=="__main__":
    hub ,robot, left_wheel, right_wheel,left_lift,right_lift = initialize_robot()
    run_task(multitask(
        sensor_logger_task(), 
        main()
    ))