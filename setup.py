"""
【ロボット初期化ファイル】
このファイルは、ロボットを使い始める前に必要な「準備作業」をまとめたものです。
料理を始める前に、材料を並べたり、調理器具を準備するのと同じように、
ロボットもプログラムを動かす前に、モーターやセンサーの設定が必要です。

【このファイルでやること】
1. ハブ（ロボットの脳みそ）の向きを設定
2. モーター（タイヤやアームを動かす装置）の設定
3. ロボットの速度やパワーの設定
4. PID制御（ロボットをまっすぐ動かすための調整機能）の設定
5. センサーの初期化

【使い方】
他のプログラムから「initialize_robot()」という関数を呼ぶだけで、
すべての準備が自動的に完了します。
"""

# ===== ライブラリのインポート =====
# LEGOロボットを動かすために必要な道具を読み込みます
from pybricks.hubs import PrimeHub          # ロボットの「脳みそ」（ハブ）を使うための道具
from pybricks.parameters import Port, Axis, Direction, Stop  # ポート、軸、方向などの設定
from pybricks.pupdevices import Motor       # モーターを使うための道具
from pybricks.robotics import DriveBase     # ロボットの移動機能を使うための道具

# ===== ハブの設定をする関数 =====
def setup_hub():
    """
    ハブ（ロボットの脳みそ）の向きを設定する関数
    
    【説明】
    ハブには「どちらが上か」「どちらが前か」を教える必要があります。
    これを正しく設定しないと、ロボットが正しく動きません。
    
    【設定内容】
    - top_side=Axis.Z : Z軸が上向き
    - front_side=Axis.X : X軸が前向き
    """
    return PrimeHub(top_side=Axis.Z, front_side=Axis.X)

# ===== モーターの設定をする関数 =====
def setup_motors():
    """
    4つのモーター（左右のタイヤ、左右のリフト）を設定する関数
    
    【説明】
    ロボットには4つのモーターがあります：
    1. 左のタイヤ用モーター
    2. 右のタイヤ用モーター
    3. 左のリフト（アーム）用モーター
    4. 右のリフト（アーム）用モーター
    
    それぞれのモーターがどのポート（差し込み口）に接続されているか、
    どちらの方向を「正」とするかを設定します。
    
    【ポートの接続】
    - Port.F : 左タイヤ（反時計回りが正の方向）
    - Port.B : 右タイヤ（時計回りが正の方向）
    - Port.E : 左リフト（時計回りが正の方向）
    - Port.A : 右リフト（時計回りが正の方向）
    """
    # 左タイヤのモーター（ポートFに接続、反時計回りが正）
    left_wheel = Motor(Port.F, positive_direction=Direction.COUNTERCLOCKWISE)
    # 右タイヤのモーター（ポートBに接続、時計回りが正）
    right_wheel = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
    # 左リフトのモーター（ポートEに接続、時計回りが正）
    left_lift = Motor(Port.E, positive_direction=Direction.CLOCKWISE)
    # 右リフトのモーター（ポートAに接続、時計回りが正）
    right_lift = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
    
    # 4つのモーターをまとめて返す
    return left_wheel, right_wheel,left_lift,right_lift

# ===== ロボットのパラメータ（動作の設定）をする関数 =====
def setup_robot_parameters(left_wheel, right_wheel, straight_speed_percent=40, turn_speed_percent=30, motor_power_percent=100):
    """
    ロボットの動く速度やパワーを設定する関数
    
    【説明】
    ロボットがどのくらいの速さで動くか、どのくらいのパワーで動くかを設定します。
    車でいうと「アクセルの踏み方」や「エンジンの出力」を決めるようなものです。
    
    【パラメータ（設定できる値）】
    - straight_speed_percent : 直進する速度（0〜100%）デフォルト40%
    - turn_speed_percent : 回転する速度（0〜100%）デフォルト30%
    - motor_power_percent : モーターのパワー（0〜100%）デフォルト100%
    
    【なぜパーセントで設定するのか？】
    100%が最大速度ですが、速すぎるとコントロールが難しくなります。
    競技に合わせて、適切な速度を選びます。
    """
    
    # ----- 速度の計算 -----
    # パーセンテージを実際の速度（mm/sやdeg/s）に変換します
    straight_rate = straight_speed_percent          # 直進速度の割合（例: 40%）
    straight_spd = 500 * (straight_rate / 100)      # 実際の速度に変換（例: 40% → 200mm/s）
    turn_rate = turn_speed_percent                  # 旋回速度の割合（例: 30%）
    turn_spd = 500 * (turn_rate / 100)              # 実際の速度に変換（例: 30% → 150deg/s）

    # 設定した速度をコンピューターの画面に表示
    print(f"速度設定: 直進={straight_speed_percent}% ({straight_spd:.0f}mm/s), 旋回={turn_speed_percent}% ({turn_spd:.0f}deg/s)")
    print(f"モーターパワー設定: {motor_power_percent}%")

    # ----- ロボットの物理的な大きさを設定 -----
    # ロボットがまっすぐ進むためには、タイヤの大きさや車軸の幅を正確に教える必要があります
    robot = DriveBase(
                    left_wheel,           # 左タイヤのモーター
                    right_wheel,          # 右タイヤのモーター
                    wheel_diameter=62,    # タイヤの直径（mm）※実際に測定した値
                    axle_track=115        # 左右のタイヤの間隔（mm）※実際に測定した値
    )
    # 注意: wheel_diameterとaxle_trackの値が正確なほど、ロボットの動きが正確になります！

    # ----- ロボットの動作速度を設定 -----
    robot.settings(
        straight_speed=straight_spd,        # 直進速度（先ほど計算した値）
        turn_rate=turn_spd,                 # 旋回速度（先ほど計算した値）
    )
    
    # ----- モーターのパワーを設定 -----
    # モーターにどれくらいの電力を送るかを設定します
    motor_power = motor_power_percent / 100.0  # パーセントを0.0〜1.0の値に変換
    left_wheel.dc(motor_power)   # 左タイヤのモーターにパワーを設定
    right_wheel.dc(motor_power)  # 右タイヤのモーターにパワーを設定
    
    # 設定が完了したロボットを返す
    return robot

# ===== PID制御の設定をする関数 =====
def setup_pid_control(robot):
    """
    PID制御を設定する関数
    
    【PID制御とは？】
    ロボットをまっすぐ正確に動かすための「自動調整機能」です。
    
    例えば、車を運転するときに、カーブでハンドルを少しずつ調整しますよね？
    PID制御は、ロボットが自動的にこの調整をしてくれる機能です。
    
    【PIDの意味】
    - P (Proportional: 比例) : 目標からどれくらいズレているかに応じて調整
    - I (Integral: 積分) : 過去のズレを積み重ねて調整
    - D (Derivative: 微分) : ズレの変化の速さに応じて調整
    
    【2種類のPID制御】
    1. 距離制御 (DISTANCE) : 「どれくらい進むか」を正確にコントロール
    2. 方向制御 (HEADING) : 「どの方向を向くか」を正確にコントロール
    
    【注意】
    下の数値（KP, KI, KD）は「ゲイン」と呼ばれ、調整の強さを決めます。
    この数値を変えると、ロボットの動きが変わります。
    うまく動かない場合は、これらの数値を調整する必要があります。
    """
    
    # ----- 距離制御用のPIDゲイン（「進む距離」をコントロール） -----
    DISTANCE_KP = 1000   # P（比例）ゲイン: 目標との距離差に対する反応の強さ
    DISTANCE_KI = 50     # I（積分）ゲイン: 過去のズレを修正する強さ
    DISTANCE_KD = 10     # D（微分）ゲイン: 急な変化を抑える強さ

    # ----- 方向制御用のPIDゲイン（「向き」をコントロール） -----
    HEADING_KP = 2000    # P（比例）ゲイン: 目標との角度差に対する反応の強さ
    HEADING_KI = 50      # I（積分）ゲイン: 過去のズレを修正する強さ
    HEADING_KD = 100     # D（微分）ゲイン: 急な変化を抑える強さ

    # ----- ロボットにPIDゲインを設定 -----
    # 距離制御のPIDゲインを設定
    robot.distance_control.pid(
        kp=DISTANCE_KP,
        ki=DISTANCE_KI,
        kd=DISTANCE_KD
    )

    # 方向制御のPIDゲインを設定
    robot.heading_control.pid(
        kp=HEADING_KP,
        ki=HEADING_KI,
        kd=HEADING_KD
    )

# ===== センサーを初期化する関数 =====
def initialize_sensors(hub, robot):
    """
    センサーとジャイロ（方向センサー）を初期化する関数
    
    【説明】
    ロボットには「ジャイロセンサー」という、スマートフォンの画面回転機能と同じような
    センサーが付いています。これは「ロボットがどちらを向いているか」を測定します。
    
    【やること】
    1. ジャイロセンサーを使用する設定にする
    2. 方向を0度（まっすぐ）にリセット
    3. ロボットの走行距離などをリセット
    
    【なぜ必要？】
    プログラムを実行する前に、「今がスタート地点」だと教える必要があります。
    これをしないと、前のプログラムの影響が残ってしまいます。
    """
    robot.use_gyro(True)           # ジャイロセンサーを使う設定にする
    hub.imu.reset_heading(0)       # 方向を0度（正面）にリセット
    robot.reset()                  # ロボットの走行距離や回転角度をリセット

# ===== モーターの角度をリセットする関数 =====
def reset_motor_angles(left_wheel, right_wheel, left_lift, right_lift):
    """
    すべてのモーターの角度を0度にリセットする関数
    
    【説明】
    モーターは回転した角度を記録しています。
    例えば、タイヤが360度回転したら「1回転した」と記録されます。
    
    この関数は、すべてのモーターの角度を0度に戻します。
    時計の針を12時の位置に戻すようなイメージです。
    
    【対象モーター】
    - 左タイヤ
    - 右タイヤ
    - 左リフト（アーム）
    - 右リフト（アーム）
    
    【なぜ必要？】
    プログラムを実行する前に、モーターの角度をリセットしないと、
    「前回どこまで回転したか」の情報が残ってしまい、正確に動きません。
    """
    left_wheel.reset_angle(0)      # 左タイヤのモーターを0度にリセット
    right_wheel.reset_angle(0)     # 右タイヤのモーターを0度にリセット
    left_lift.reset_angle(0)       # 左リフトのモーターを0度にリセット
    right_lift.reset_angle(0)      # 右リフトのモーターを0度にリセット
    print("✓ モーター角度リセット完了: 全モーター=0°")

# ===== ロボット全体を初期化する関数（メイン関数） =====
def initialize_robot(straight_speed_percent=60, turn_speed_percent=30, motor_power_percent=100):
    """
    ロボットを使う準備を全部まとめて行う関数
    
    【説明】
    この関数は、上で定義した5つの関数をすべて実行して、
    ロボットを使えるようにします。
    
    料理で言えば、「材料を切る」「調味料を準備する」「火をつける」など、
    すべての準備作業を一度に済ませる関数です。
    
    【パラメータ（設定できる値）】
    - straight_speed_percent : 直進速度（0〜100%）デフォルト40%
    - turn_speed_percent : 回転速度（0〜100%）デフォルト30%
    - motor_power_percent : モーターパワー（0〜100%）デフォルト100%
    
    【実行する処理（順番通り）】
    1. ハブの設定
    2. モーターの設定
    3. ロボットパラメータの設定
    4. PID制御の設定
    5. センサーの初期化
    6. モーター角度のリセット
    
    【返り値（戻ってくる値）】
    この関数は、以下の6つの情報を返します：
    - hub : ハブ（ロボットの脳みそ）
    - robot : ロボット全体のオブジェクト
    - left_wheel : 左タイヤのモーター
    - right_wheel : 右タイヤのモーター
    - left_lift : 左リフトのモーター
    - right_lift : 右リフトのモーター
    
    【使い方の例】
    他のプログラムから以下のように使います：
    hub, robot, left_wheel, right_wheel, left_lift, right_lift = initialize_robot()
    """
    print("=== ロボット初期化開始 ===")
    
    # ----- ステップ1: ハブの設定 -----
    hub = setup_hub()
    print("✓ ハブ設定完了")
    
    # ----- ステップ2: モーターの設定 -----
    left_wheel, right_wheel,left_lift,right_lift= setup_motors()
    print("✓ モーター設定完了")
    
    # ----- ステップ3: ロボットパラメータの設定 -----
    robot = setup_robot_parameters(left_wheel, right_wheel, straight_speed_percent, turn_speed_percent, motor_power_percent)
    print("✓ ロボットパラメータ設定完了")
    
    # ----- ステップ4: PID制御の設定 -----
    setup_pid_control(robot)
    print("✓ PID制御設定完了")
    
    # ----- ステップ5: センサーの初期化 -----
    initialize_sensors(hub, robot)
    print("✓ センサー初期化完了")
    
    # ----- ステップ6: モーター角度のリセット -----
    reset_motor_angles(left_wheel, right_wheel, left_lift, right_lift)
    
    print("=== ロボット初期化完了 ===")
    
    # ----- すべての設定情報を返す -----
    return hub ,robot, left_wheel, right_wheel,left_lift,right_lift