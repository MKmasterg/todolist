""" NOTE: CLI interface is deprecated.
"""
from copy import copy
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from core.services import (get_project_list, get_project_tasks, create_project, get_project_from_name,
                           add_task_to_project, delete_project, get_task_by_uuid_in_project, delete_task_from_project,
                           update_task_elements, update_project)
from core.jobs import autoclose_overdue_tasks
from data.database import AsyncSessionLocal

# Global variables to control the autoclose background job (async)
_autoclose_task: Optional[asyncio.Task] = None
_autoclose_stop_event: asyncio.Event = asyncio.Event()


async def ai_input(prompt: str = "") -> str:
    """Run blocking input() in a thread to avoid blocking the event loop."""
    return await asyncio.to_thread(input, prompt)


async def handle_command(db: AsyncSession, command: str, args: List[str]) -> None:
    """
    CLI interface is deprecated
    
    Handle CLI commands.

    :param db: Database session
    :param command: The command to execute (e.g., 'get', 'add', 'delete')
    :param args: List of arguments for the command
    """
    if not command:
        print_error("No command provided")
        return
    if command == "get":
        await _handle_get_command(db, args)
    elif command == "add":
        await _handle_add_command(db, args)
    elif command == "delete":
        await _handle_delete_command(db, args)
    elif command == "update":
        await _handle_update_command(db, args)
    elif command == "tasks:autoclose-overdue":
        _handle_autoclose_overdue(db)
    elif command == "tasks:autoclose-stop":
        _handle_autoclose_stop()
    elif command == "help":
        print_help()
    else:
        print_error(f"Unknown command: {command}")
        print_help()


async def _handle_get_command(db: AsyncSession, args: List[str]) -> None:
    """
    CLI interface is deprecated
    
    Handle 'get' commands.
    """
    if not args:
        print_error("No resource specified for 'get' command")
        return

    resource = args[0].lower()
    if resource == "projects":
        await _handle_get_projects(db)
    elif resource == "tasks":
        if len(args) < 2:
            print_error("Project name required for 'get tasks' command")
            return
        await _handle_get_tasks(db, args[1])
    else:
        print_error(f"Unknown resource: {resource}")


async def _handle_add_command(db: AsyncSession, args: List[str]) -> None:
    """
    CLI interface is deprecated
    
    Handle 'add' commands.
    """
    if not args:
        print_error("No resource specified for 'add' command")
        return

    resource = args[0].lower()
    if resource == "project":
        name = (await ai_input("Please enter project name (at most 30 characters):\n")).strip()
        description = (await ai_input("Please enter project description (optional, at most 150 characters):\n")).strip()

        try:
            await create_project(db, name=name, desc=description)
        except Exception as e:
            print_error(f"Error creating project: {str(e)}")
            return

        print_info(f"Add project: {name}")

    elif resource == "task":
        project_name = (await ai_input("Please enter project name to add task to:\n")).strip()
        try:
            selected_project = await get_project_from_name(db, project_name)
            if not selected_project:
                print_error(f"Project '{project_name}' not found")
                return
        except Exception as e:
            print_error(f"Error finding project: {str(e)}")
            return

        title = (await ai_input("Please enter task title (at most 30 characters):\n")).strip()
        description = (await ai_input("Please enter task description (optional, at most 150 characters):\n")).strip()
        status = (await ai_input("Please enter task status (todo, doing, done) [default: todo]:\n")).strip() or "todo"
        deadline_input = (await ai_input("Please enter task deadline (YYYY-MM-DD) [optional]:\n")).strip()

        deadline = None
        if deadline_input:
            try:
                deadline = datetime.strptime(deadline_input, "%Y-%m-%d")
            except ValueError:
                print_error("Invalid deadline format. Please use YYYY-MM-DD")
                return

        try:
            await add_task_to_project(db, selected_project, title=title, description=description, status=status,
                                deadline=deadline)
        except Exception as e:
            print_error(f"Error adding task: {str(e)}")
            return

        print_info(f"Add task to project {title}: {project_name}")
    else:
        print_error(f"Unknown resource: {resource}")


async def _handle_delete_command(db: AsyncSession, args: List[str]) -> None:
    """
    CLI interface is deprecated
    
    Handle 'delete' commands.
    :param db: Database session
    :param args: List of arguments for the delete command
    """
    if not args:
        print_error("No resource specified for 'delete' command")
        return

    resource = args[0].lower()
    if resource == "project":
        if len(args) < 2:
            print_error("Project name required")
            return
        try:
            project = await get_project_from_name(db, args[1])  # Verify project exists
            if not project:
                print_error(f"Project '{args[1]}' not found")
                return
        except Exception as e:
            print_error(f"Error finding project: {str(e)}")
            return

        try:
            await delete_project(db, project)
        except Exception as e:
            print_error(f"Error deleting project: {str(e)}")
            return

        print_info(f"Delete project: {args[1]}")

    elif resource == "task":
        if len(args) < 3:
            print_error("Project name and task ID required")
            return
        try:
            project = await get_project_from_name(db, args[1])
            if not project:
                print_error(f"Project '{args[1]}' not found")
                return
            task = await get_task_by_uuid_in_project(db, args[1], args[2])  # Verify task exists
            if not task:
                print_error(f"Task '{args[2]}' not found")
                return
        except Exception as e:
            print_error(f"Error finding task: {str(e)}")
            return

        try:
            await delete_task_from_project(db, project, args[2])
        except Exception as e:
            print_error(f"Error deleting task: {str(e)}")
            return

        print_info(f"Delete task {args[2]} from project {args[1]}")
    else:
        print_error(f"Unknown resource: {resource}")


async def _handle_update_command(db: AsyncSession, args: List[str]) -> None:
    """
    CLI interface is deprecated
    
    Handle 'update' commands.
    :param db: Database session
    :param args: List of arguments for the update command
    """
    if not args:
        print_error("No resource specified for 'update' command")
        return

    resource = args[0].lower()
    if resource == "task":
        if len(args) < 3:
            print_error("Project name and task ID required")
            return
        try:
            task = await get_task_by_uuid_in_project(db, args[1], args[2])  # Verify task exists
            if not task:
                print_error(f"Task '{args[2]}' not found")
                return
            project = await get_project_from_name(db, args[1])
            if not project:
                print_error(f"Project '{args[1]}' not found")
                return
        except Exception as e:
            print_error(f"Error finding task: {str(e)}")
            return

        new_name = (await ai_input("Please enter new task name [leave blank if want unchanged]:\n")).strip()
        new_description = (await ai_input("Please enter new task description [leave blank if want unchanged]:\n")).strip()
        new_status = (await ai_input("Please enter new task status (todo, doing, done) [leave blank if want unchanged]:\n")).strip()
        new_deadline_str = (await ai_input("Please enter new task deadline (YYYY-MM-DD) [leave blank if want unchanged]:\n")).strip()

        new_task = copy(task)

        try:
            if new_name:
                new_task.set_title(new_name)
            if new_description:
                new_task.set_description(new_description)
            if new_status:
                new_task.set_status(new_status)
            if new_deadline_str:
                new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
                new_task.set_deadline(new_deadline)
        except Exception as e:
            print_error(f"Error updating task: {str(e)}")
            return

        # Update the task in the project
        try:
            await update_task_elements(db, project, args[2], new_task.get_title(), new_task.get_description(), 
                               new_task.get_status(), new_task.get_deadline())
        except Exception as e:
            print_error(f"Error saving updated task: {str(e)}")
            return

        print_info(f"Update task {args[2]} in project {args[1]}")

    elif resource == "task_status":
        if len(args) < 4:
            print_error("Project name, task ID, and new status required")
            return
        try:
            project = await get_project_from_name(db, args[1])
            if not project:
                print_error(f"Project '{args[1]}' not found")
                return
            task = await get_task_by_uuid_in_project(db, args[1], args[2])  # Verify task exists
            if not task:
                print_error(f"Task '{args[2]}' not found")
                return
            new_status = args[3]
        except Exception as e:
            print_error(f"Error finding task or validating status: {str(e)}")
            return

        try:
            task.set_status(new_status)
            await update_task_elements(db, project, args[2], task.get_title(), task.get_description(), 
                               task.get_status(), task.get_deadline())
        except Exception as e:
            print_error(f"Error updating task status: {str(e)}")
            return

        print_info(f"Update task {args[2]} status in project {args[1]} to {new_status}")

    elif resource == "project":
        if len(args) < 2:
            print_error("Project name required")
            return
        try:
            project = await get_project_from_name(db, args[1])
            if not project:
                print_error(f"Project '{args[1]}' not found")
                return
        except Exception as e:
            print_error(f"Error finding project: {str(e)}")
            return

        new_name = (await ai_input("Please enter new project name [leave blank if want unchanged]:\n")).strip()
        new_description = (await ai_input("Please enter new project description [leave blank if want unchanged]:\n")).strip()
        old_name = project.get_name()
        try:
            if new_name:
                project.set_name(new_name)
            if new_description:
                project.set_description(new_description)

            await update_project(db, old_name, project)

        except Exception as e:
            print_error(f"Error updating project: {str(e)}")
            return

        print_info(f"Update project: {args[1]}")

    else:
        print_error(f"Unknown resource: {resource}")


async def _handle_autoclose_overdue(db: AsyncSession) -> None:
    """
    CLI interface is deprecated

    Start auto-close of overdue tasks on a recurring interval (async).
    """
    global _autoclose_task, _autoclose_stop_event

    # If a task is already running, offer to stop it first
    if _autoclose_task and not _autoclose_task.done():
        print_info("Auto-close job is already running in the background")
        response = (await ai_input("Do you want to stop the current job and start a new one? (yes/no):\n")).strip().lower()
        if response not in ['yes', 'y']:
            return
        _autoclose_stop_event.set()
        try:
            await asyncio.wait_for(_autoclose_task, timeout=2)
        except asyncio.TimeoutError:
            # let it be cancelled on next iteration
            pass
        _autoclose_stop_event.clear()

    interval_input = (await ai_input("Please enter the interval in seconds for auto-closing overdue tasks (e.g., 60):\n")).strip()
    try:
        interval = int(interval_input)
        if interval <= 0:
            print_error("Interval must be a positive number")
            return
    except ValueError:
        print_error("Invalid interval. Please enter a number in seconds")
        return

    _autoclose_stop_event.clear()
    _autoclose_task = asyncio.create_task(_autoclose_background_job(interval))

    print_success(f"Auto-close job started! Running every {interval} seconds in the background")
    print_info("The job will continue running and display updates here. Type 'tasks:autoclose-stop' to stop it.")


async def _autoclose_background_job(interval: int) -> None:
    """
    CLI interface is deprecated

    Background async job that runs autoclose_overdue_tasks at specified intervals.
    """
    while not _autoclose_stop_event.is_set():
        try:
            async with AsyncSessionLocal() as session:
                await autoclose_overdue_tasks(session)
        except Exception as e:
            print_error(f"Error in auto-close background job: {str(e)}")
        try:
            await asyncio.wait_for(_autoclose_stop_event.wait(), timeout=interval)
        except asyncio.TimeoutError:
            # timeout expired, loop and run again
            continue


async def _handle_autoclose_stop() -> None:
    """
    CLI interface is deprecated

    Stop the running auto-close background job (async).
    """
    global _autoclose_task, _autoclose_stop_event

    if not _autoclose_task or _autoclose_task.done():
        print_info("No auto-close job is currently running")
        return

    print_info("Stopping auto-close background job...")
    _autoclose_stop_event.set()
    try:
        await asyncio.wait_for(_autoclose_task, timeout=5)
    except asyncio.TimeoutError:
        if not _autoclose_task.done():
            _autoclose_task.cancel()

    if _autoclose_task.done():
        print_success("Auto-close job stopped successfully")
    else:
        print_error("Failed to stop the auto-close job")


async def _handle_get_projects(db: AsyncSession) -> None:
    """
    CLI interface is deprecated
    
    Retrieve and display all projects.
    
    :param db: Database session
    """
    try:
        projects = await get_project_list(db)
        if not projects:
            print_info("No projects found")
            return None

        print_success(f"Found {len(projects)} project(s):")
        for idx, project in enumerate(projects, 1):
            print(f"  {idx}. {project.get_name()} - {project.get_description()}")
            tasks = await get_project_tasks(db, project)
            print(f"     Tasks: {len(tasks)}")
            print("     " + "-" * 40)

    except Exception as e:
        print_error(f"Error retrieving projects: {str(e)}")
        return None


async def _handle_get_tasks(db: AsyncSession, project_name: str) -> Optional[List]:
    """
    CLI interface is deprecated
    
    Retrieve and display tasks for a specific project.
    
    :param db: Database session
    :param project_name: The name of the project to retrieve tasks from.
    :return: List of tasks if successful, None otherwise.
    """
    try:
        project = await get_project_from_name(db, project_name)
        if not project:
            print_error(f"Project '{project_name}' not found")
            return None
        tasks = await get_project_tasks(db, project)
        tasks.reverse()

        if not tasks:
            print_info(f"No tasks found for project '{project_name}'")
            return None

        print_success(f"Tasks in project '{project_name}':")
        for _, task in enumerate(tasks, 1):
            print(f"  {task.get_uuid()}. {task.get_title()} - {task.get_status()}")
            if task.get_deadline():
                print(f"     Deadline: {task.get_deadline()}")
            print(f"     Description: {task.get_description()}")
            print("     " + "-" * 40)

        return tasks
    except Exception as e:
        print_error(f"Error retrieving tasks: {str(e)}")
        return None


def print_success(message: str) -> None:
    """
    CLI interface is deprecated
    
    Print a success message.
    :param message: The success message to print.
    """
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """
    CLI interface is deprecated
    
    Print an error message.
    :param message: The error message to print.
    """
    print(f"✗ Error: {message}")


def print_info(message: str) -> None:
    """
    CLI interface is deprecated
    
    Print an informational message.
    :param message: The informational message to print.
    """
    print(f"ℹ {message}")


def print_help() -> None:
    """
    CLI interface is deprecated
    
    Display help information about available commands.
    """
    help_text = """
Todo List CLI - Available Commands:

  get projects                                 - List all projects
  get tasks "<project>"                        - List all tasks in a project
  add project                                  - Add a new project
  add task                                     - Add a new task to a project
  delete project "<name>"                      - Delete a project
  delete task "<project>" <id>                 - Delete a task from a project
  update task "<project>" <id>                 - Update a task in a project
  update task_status "<project>" <id> <status> - Update a task's status
  update project "<name>"                      - Update a project's name or description
  tasks:autoclose-overdue                      - Start auto-close job for overdue tasks (runs at intervals)
  tasks:autoclose-stop                         - Stop the running auto-close background job
  help                                         - Show this help message
  exit                                         - Exit the CLI
"""
    print(help_text)
