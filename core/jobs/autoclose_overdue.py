"""
Job to automatically close overdue tasks.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from data.models import TaskModel
from core.models import Status


def autoclose_overdue_tasks(db: Session) -> dict:
    """
    Automatically close all overdue tasks.
    
    Logic:
    - If deadline < now and status != 'done'
    - Then mark the task as 'done' and set updated_at to now
    
    :param db: Database session
    :return: Dictionary with count of closed tasks and their UUIDs
    """
    now = datetime.now()
    
    # Query all tasks where deadline is past and status is not 'done'
    overdue_tasks = db.query(TaskModel).filter(
        TaskModel.deadline < now,
        TaskModel.status != Status.DONE
    ).all()
    
    closed_count = 0
    closed_uuids = []
    
    for task in overdue_tasks:
        task.status = Status.DONE
        task.updated_at = now
        closed_count += 1
        closed_uuids.append(str(task.uuid))
    
    if closed_count > 0:
        db.commit()
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Auto-closed {closed_count} overdue task(s)")
        for uuid in closed_uuids:
            print(f"  - Task UUID: {uuid}")
    else:
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] No overdue tasks to close")
    
    return {
        'closed_count': closed_count,
        'closed_uuids': closed_uuids,
        'timestamp': now
    }
