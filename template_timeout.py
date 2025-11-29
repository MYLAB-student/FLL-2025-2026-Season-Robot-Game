"""
タイムアウト機能テンプレート

ロボットが壁にぶつかったり、想定外の状況で停止した場合でも、
指定した時間が経過したら次の行動に移るための汎用関数を提供します。

使い方:
    from template_timeout import wait_with_timeout, run_with_timeout
"""

from pybricks.tools import wait, StopWatch


async def wait_with_timeout(robot_action, timeout_ms=3000, check_interval_ms=10):
    """
    ロボットの動作をタイムアウト付きで待機する関数
    
    この関数は、ロボットの動作が完了するか、タイムアウト時間が経過するまで待機します。
    壁にぶつかって動作が完了しない場合でも、タイムアウトで次の処理に進めます。
    
    Args:
        robot_action: 実行中のロボット動作（wait=Falseで開始した動作）
        timeout_ms: タイムアウト時間（ミリ秒）。デフォルトは3000ms（3秒）
        check_interval_ms: 動作完了をチェックする間隔（ミリ秒）。デフォルトは10ms
    
    Returns:
        bool: 動作が正常に完了した場合はTrue、タイムアウトした場合はFalse
    
    使用例:
        # 直進動作を非同期で開始
        robot.straight(500, wait=False)
        # タイムアウト付きで待機（3秒でタイムアウト）
        success = await wait_with_timeout(robot, timeout_ms=3000)
        if success:
            print("動作完了")
        else:
            print("タイムアウト - 次の動作へ")
    """
    timeout = StopWatch()
    timeout.reset()
    
    while timeout.time() < timeout_ms:
        # 動作が完了したかチェック
        if robot_action.done():
            print(f"✓ 動作完了 ({timeout.time()}ms)")
            return True
        # まだ動作中の場合、少し待機してから再チェック
        await wait(check_interval_ms)
    
    # タイムアウトした場合
    print(f"⚠ タイムアウト ({timeout_ms}ms経過) - 次の動作へ移行")
    robot_action.stop()  # 動作を停止
    return False


async def run_with_timeout(action_func, timeout_ms=5000, action_name="動作"):
    """
    任意のロボット動作をタイムアウト付きで実行する関数
    
    この関数は、指定された動作関数を実行し、タイムアウト時間内に完了するまで待機します。
    より高レベルの抽象化で、動作の開始から完了までを管理します。
    
    Args:
        action_func: 実行する非同期関数
        timeout_ms: タイムアウト時間（ミリ秒）。デフォルトは5000ms（5秒）
        action_name: 動作の名前（ログ表示用）
    
    Returns:
        bool: 動作が正常に完了した場合はTrue、タイムアウトした場合はFalse
    
    使用例1（直進動作）:
        success = await run_with_timeout(
            lambda: robot.straight(500),
            timeout_ms=3000,
            action_name="直進500mm"
        )
        
    使用例2（回転動作）:
        success = await run_with_timeout(
            lambda: robot.turn(90),
            timeout_ms=2000,
            action_name="90度回転"
        )
    """
    timeout = StopWatch()
    timeout.reset()
    
    print(f"開始: {action_name}")
    
    # 動作を開始
    action_task = action_func()
    
    try:
        while timeout.time() < timeout_ms:
            # 動作が完了したかチェック
            try:
                await action_task
                print(f"✓ {action_name}完了 ({timeout.time()}ms)")
                return True
            except:
                # まだ実行中
                await wait(10)
        
        # タイムアウトした場合
        print(f"⚠ {action_name}タイムアウト ({timeout_ms}ms経過) - 次の動作へ")
        return False
        
    except Exception as e:
        print(f"✗ {action_name}エラー: {e}")
        return False


async def safe_straight(robot, distance_mm, timeout_ms=3000, speed=None):
    """
    タイムアウト付きの安全な直進動作
    
    Args:
        robot: DriveBaseオブジェクト
        distance_mm: 移動距離（mm）
        timeout_ms: タイムアウト時間（ミリ秒）
        speed: 速度（指定しない場合はデフォルト設定を使用）
    
    Returns:
        bool: 動作が正常に完了した場合はTrue、タイムアウトした場合はFalse
    
    使用例:
        # 500mm直進、3秒でタイムアウト
        await safe_straight(robot, 500, timeout_ms=3000)
    """
    timeout = StopWatch()
    timeout.reset()
    
    # 動作を非同期で開始
    if speed is not None:
        robot.straight(distance_mm, wait=False)
        # 速度設定がある場合は一時的に変更
        # 注: Pybricksでは動作開始後の速度変更は不可
    else:
        robot.straight(distance_mm, wait=False)
    
    # タイムアウト付きで待機
    result = await wait_with_timeout(robot, timeout_ms)
    
    return result


async def safe_turn(robot, angle_deg, timeout_ms=3000, rate=None):
    """
    タイムアウト付きの安全な回転動作
    
    Args:
        robot: DriveBaseオブジェクト
        angle_deg: 回転角度（度）
        timeout_ms: タイムアウト時間（ミリ秒）
        rate: 回転速度（指定しない場合はデフォルト設定を使用）
    
    Returns:
        bool: 動作が正常に完了した場合はTrue、タイムアウトした場合はFalse
    
    使用例:
        # 90度回転、2秒でタイムアウト
        await safe_turn(robot, 90, timeout_ms=2000)
    """
    timeout = StopWatch()
    timeout.reset()
    
    # 動作を非同期で開始
    robot.turn(angle_deg, wait=False)
    
    # タイムアウト付きで待機
    result = await wait_with_timeout(robot, timeout_ms)
    
    return result


async def safe_curve(robot, radius_mm, angle_deg, timeout_ms=3000):
    """
    タイムアウト付きの安全なカーブ動作
    
    Args:
        robot: DriveBaseオブジェクト
        radius_mm: カーブ半径（mm）
        angle_deg: カーブ角度（度）
        timeout_ms: タイムアウト時間（ミリ秒）
    
    Returns:
        bool: 動作が正常に完了した場合はTrue、タイムアウトした場合はFalse
    
    使用例:
        # 半径200mmで90度カーブ、3秒でタイムアウト
        await safe_curve(robot, 200, 90, timeout_ms=3000)
    """
    timeout = StopWatch()
    timeout.reset()
    
    # 動作を非同期で開始
    robot.curve(radius_mm, angle_deg, wait=False)
    
    # タイムアウト付きで待機
    result = await wait_with_timeout(robot, timeout_ms)
    
    return result


async def safe_motor_angle(motor, speed, angle_deg, timeout_ms=3000, motor_name="モーター"):
    """
    タイムアウト付きの安全なモーター角度動作（リフトやアーム用）
    
    Args:
        motor: Motorオブジェクト
        speed: 回転速度（deg/s）
        angle_deg: 回転角度（度）
        timeout_ms: タイムアウト時間（ミリ秒）
        motor_name: モーター名（ログ表示用）
    
    Returns:
        bool: 動作が正常に完了した場合はTrue、タイムアウトした場合はFalse
    
    使用例:
        # 左リフトを300速度で180度回転、2秒でタイムアウト
        await safe_motor_angle(left_lift, 300, 180, timeout_ms=2000, motor_name="左リフト")
    """
    timeout = StopWatch()
    timeout.reset()
    
    print(f"開���: {motor_name} {angle_deg}度回転")
    
    # 動作を非同期で開始
    motor.run_angle(speed, angle_deg, wait=False)
    
    while timeout.time() < timeout_ms:
        # 動作が完了したかチェック
        if motor.done():
            print(f"✓ {motor_name}動作完了 ({timeout.time()}ms)")
            return True
        # まだ動作中の場合、少し待機してから再チェック
        await wait(10)
    
    # タイムアウトした場合
    print(f"⚠ {motor_name}タイムアウト ({timeout_ms}ms経過) - 次の動作へ")
    motor.stop()  # モーターを停止
    return False


# ==========================================
# 使用例のコード（コメントアウト）
# ==========================================
"""
使用例1: 基本的な使い方（wait_with_timeout）
-----------------------------------------
from template_timeout import wait_with_timeout

async def run(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    # 直進動作を非同期で開始
    robot.straight(500, wait=False)
    # タイムアウト付きで待機（3秒でタイムアウト）
    success = await wait_with_timeout(robot, timeout_ms=3000)
    
    if success:
        print("直進完了！")
    else:
        print("タイムアウトしました。次の動作へ")
    
    # 次の動作
    await robot.turn(90)


使用例2: 簡単な使い方（safe_straight、safe_turn）
-----------------------------------------
from template_timeout import safe_straight, safe_turn, safe_motor_angle

async def run(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    # 500mm直進（3秒でタイムアウト）
    await safe_straight(robot, 500, timeout_ms=3000)
    
    # 90度回転（2秒でタイムアウト）
    await safe_turn(robot, 90, timeout_ms=2000)
    
    # 左リフトを動かす（2秒でタイムアウト）
    await safe_motor_angle(left_lift, 300, 180, timeout_ms=2000, motor_name="左リフト")
    
    # カーブ（3秒でタイムアウト）
    await safe_curve(robot, 200, 90, timeout_ms=3000)


使用例3: 既存コードの置き換え（run1_M01_M02_kanna.pyの例）
-----------------------------------------
# 変更前:
robot.straight(205, wait=False)
timeout = StopWatch()
timeout.reset()
while timeout.time() < 3000:
    if not robot.done():
        await wait(10)
    else:
        break

# 変更後:
from template_timeout import safe_straight
await safe_straight(robot, 205, timeout_ms=3000)


使用例4: カスタムタイムアウト付きシーケンス
-----------------------------------------
from template_timeout import safe_straight, safe_turn, safe_motor_angle

async def run(hub, robot, left_wheel, right_wheel, left_lift, right_lift):
    # M01ミッション
    await safe_straight(robot, 590, timeout_ms=4000)  # 長距離なので4秒
    await safe_straight(robot, -120, timeout_ms=2000)
    
    # M02ミッション
    await safe_turn(robot, 40, timeout_ms=2000)
    await safe_straight(robot, 220, timeout_ms=3000)
    await safe_turn(robot, -85, timeout_ms=2000)
    
    # 壁にぶつかる可能性がある動作は短めのタイムアウト
    await safe_straight(robot, 205, timeout_ms=2000)  # 2秒でタイムアウト
    
    # 次の動作
    await safe_straight(robot, -210, timeout_ms=3000)
    await safe_turn(robot, -45, timeout_ms=2000)
    
    print("ミッション完了！")
"""

