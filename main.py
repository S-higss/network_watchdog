import schedule, time, datetime, sys, subprocess
from src.ping_sender import ping_sender
from src.mail_sender import down_mail_sender, up_mail_sender
from domain.consts import SystemConstants
from lib.config import load_config
config = load_config(SystemConstants.config)
config_secret = load_config(SystemConstants.config_secret)
PREVIOUS_STATUS = True

def schedule_jobs(ip=0):
    # Get the current time
    now = datetime.datetime.now()
    
    # Calculate the next 10-minute interval time
    next_run_minute = 10 * ((now.minute // 10) + 1)
    next_run_hour = now.hour + (next_run_minute // 60)
    next_run_minute %= 60
    next_run_hour %= 24

    # Display the next 10-minute interval time
    next_run_time = now.replace(hour=next_run_hour, minute=next_run_minute, second=0, microsecond=0)
    print(f"Every 10min's schedules start at: {next_run_time.strftime('%H:%M')}")
    
    # Schedule jobs at 10-minute intervals every hour
    for run_minutes in range(0, 60, 10):
        schedule.every().hour.at(f":{run_minutes:02}").do(job_and_display_next_run_time, run_minutes=run_minutes, ip=ip)

def job_and_display_next_run_time(run_minutes=0, ip=0):
    global PREVIOUS_STATUS
    monitor = ping_sender(ip)
    if monitor:
        if not PREVIOUS_STATUS:
            print("Target PC is up!")
            up_mail_sender(ip)
        PREVIOUS_STATUS = True
    else:
        if PREVIOUS_STATUS:
            print("Target PC is down!")
            # Send an email
            down_mail_sender(ip)
        PREVIOUS_STATUS = False

    next_run_minutes = run_minutes + 10
    if next_run_minutes >= 60:
        next_run_minutes = 0
        hour = 1
    else:
        hour = 0
    now = datetime.datetime.now()
    next_run_time = now.replace(minute=next_run_minutes, second=0, microsecond=0) + datetime.timedelta(hours=hour)

    print(f"Next run time at: {next_run_time.strftime('%H:%M')}")

def main(ip=0):
    if ip == 0:
        ip = config_secret["IP"]["PC1"]
    schedule_jobs(ip)

    # Execute scheduled jobs
    while True:
        try:
            schedule.run_pending()
            sys.stdout.flush()
            time.sleep(1)
        except KeyboardInterrupt:
            # Terminate the program when Ctrl+C is pressed
            print("Terminating the program...")
            break
        except Exception as e:
            # Error handling for unexpected errors
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    try:
        IP = sys.argv[1]
        if IP:
            print(
                "\033[31m"
                + f"INFO: Check the target PC with {IP}"
                + "\033[0m"
            )
            main(IP)
    except Exception:
        Anonym_ok = 0
        debug = 0
    main()