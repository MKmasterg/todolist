"""
Background scheduler for periodic tasks.

This script runs as a separate process and executes scheduled jobs.
Default: Runs autoclose_overdue_tasks every 15 minutes.
"""
import schedule
import time
import argparse
from datetime import datetime
from data.database import SessionLocal
from core.jobs import autoclose_overdue_tasks


def run_autoclose_job():
    """Wrapper to run the autoclose job with a database session."""
    db = SessionLocal()
    try:
        autoclose_overdue_tasks(db)
    except Exception as e:
        print(f"[ERROR] Failed to run autoclose job: {e}")
    finally:
        db.close()


def main():
    """Main scheduler loop."""
    parser = argparse.ArgumentParser(description='Todo List Background Scheduler')
    parser.add_argument(
        '--interval',
        type=int,
        default=15,
        help='Interval in minutes to run the autoclose job (default: 15)'
    )
    args = parser.parse_args()
    
    interval = args.interval
    
    print("=" * 60)
    print("Todo List Background Scheduler Started")
    print("=" * 60)
    print(f"Job: Auto-close overdue tasks")
    print(f"Interval: Every {interval} minute(s)")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the scheduler\n")
    
    # Schedule the job
    schedule.every(interval).minutes.do(run_autoclose_job)
    
    # Run once immediately on startup
    print("Running initial check...")
    run_autoclose_job()
    print()
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
        print("=" * 60)


if __name__ == "__main__":
    main()
