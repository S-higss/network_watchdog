import schedule, time, datetime, sys, subprocess
from src.ping_sender import ping_sender
import src.mailer
from domain.consts import SystemConstants
from lib.config import load_config
config = load_config(SystemConstants.config)
PREVIOUS_STATUS = False

def schedule_jobs(ip=0):
    # 現在の時刻を取得
    now = datetime.datetime.now()
    
    # 次の10分単位の時刻を計算
    next_run_minute = 10 * ((now.minute // 10) + 1)
    next_run_hour = now.hour + (next_run_minute // 60)
    next_run_minute %= 60
    next_run_hour %= 24

    # 次の10分単位の時刻を表示
    next_run_time = now.replace(hour=next_run_hour, minute=next_run_minute, second=0, microsecond=0)
    print(f"Every 10min's schedules start at: {next_run_time.strftime('%H:%M')}")
    
    # 毎時10分間隔でジョブをスケジュール
    for run_minutes in range(0, 60, 10):
        schedule.every().hour.at(f":{run_minutes:02}").do(job_and_display_next_run_time, run_minutes=run_minutes, ip=ip)

def job_and_display_next_run_time(run_minutes=0, ip=0):
    process = True
    # 実際のジョブを実行

    monitor = ping_sender(ip)       # Gmailよりファイル自動取得
    if monitor:
        pass
    else:
        print("Target PC is down!")

        process = False

    next_run_minutes = run_minutes + 10
    if next_run_minutes >= 60:
        next_run_minutes = 0
        hour = 1
    else:
        hour = 0
    now = datetime.datetime.now()
    next_run_time = now.replace(minute=next_run_minutes, second=0, microsecond=0) + datetime.timedelta(hours=hour)

    print(f"Next run time at: {next_run_time.strftime('%H:%M')}")

def main():
    IP = input("Please enter the IP address of the target PC: ")
    schedule_jobs(IP)

    # スケジュールされたジョブを実行
    while True:
        try:
            schedule.run_pending()
            sys.stdout.flush()
            time.sleep(1)
        except KeyboardInterrupt:
            # Ctrl+Cを押した場合、プログラムを終了
            print("Terminating the program...")
            break
        except Exception as e:
            # 予期しないエラーが発生した場合のエラーハンドリング
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()