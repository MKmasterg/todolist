from copy import copy
from typing import List, Optional

from core.services import (get_project_list, get_project_tasks, create_project, get_project_from_name,
                           add_task_to_project, delete_project, get_task_by_uuid_in_project, delete_task_from_project,
                           update_task_elements, update_project)


def handle_command(command: str, args: List[str]) -> None:
    """
    Handle CLI commands.

    :param command: The command to execute (e.g., 'get', 'add', 'delete')
    :param args: List of arguments for the command
    """
    if not command:
        print_error("No command provided")
        return

    if command == "get":
        _handle_get_command(args)
    elif command == "add":
        _handle_add_command(args)
    elif command == "delete":
        _handle_delete_command(args)
    elif command == "update":
        _handle_update_command(args)
    elif command == "help":
        print_help()
    else:
        print_error(f"Unknown command: {command}")
        print_help()


def _handle_get_command(args: List[str]) -> None:
    """Handle 'get' commands."""
    if not args:
        print_error("No resource specified for 'get' command")
        return

    resource = args[0].lower()
    if resource == "projects":
        _handle_get_projects()
    elif resource == "tasks":
        if len(args) < 2:
            print_error("Project name required for 'get tasks' command")
            return
        _handle_get_tasks(args[1])
    else:
        print_error(f"Unknown resource: {resource}")


def _handle_add_command(args: List[str]) -> None:
    """Handle 'add' commands."""
    if not args:
        print_error("No resource specified for 'add' command")
        return

    resource = args[0].lower()
    if resource == "project":
        print("Please enter project name (at most 30 characters):")
        name = input().strip()
        print("Please enter project description (optional, at most 150 characters):")
        description = input().strip()

        try:
            create_project(name=name, desc=description)
        except Exception as e:
            print_error(f"Error creating project: {str(e)}")
            return

        print_info(f"Add project: {name}")

    elif resource == "task":
        print("Please enter project name to add task to:")
        project_name = input().strip()
        try:
            selected_project = get_project_from_name(project_name)
        except Exception as e:
            print_error(f"Error finding project: {str(e)}")
            return

        print("Please enter task title (at most 30 characters):")
        title = input().strip()
        print("Please enter task description (optional, at most 150 characters):")
        description = input().strip()
        print("Please enter task status (todo, doing, done) [default: todo]:")
        status = input().strip() or "todo"
        print("Please enter task deadline (YYYY-MM-DD) [optional]:")
        deadline_input = input().strip()

        try:
            add_task_to_project(selected_project, title=title, description=description, status=status,
                                deadline=deadline_input if deadline_input else None)
        except Exception as e:
            print_error(f"Error adding task: {str(e)}")
            return

        print_info(f"Add task to project {title}: {project_name}")
    else:
        print_error(f"Unknown resource: {resource}")


def _handle_delete_command(args: List[str]) -> None:
    """Handle 'delete' commands.
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
            project = get_project_from_name(args[1])  # Verify project exists
        except Exception as e:
            print_error(f"Error finding project: {str(e)}")
            return

        try:
            delete_project(project)
        except Exception as e:
            print_error(f"Error deleting project: {str(e)}")
            return

        print_info(f"Delete project: {args[1]}")

    elif resource == "task":
        if len(args) < 3:
            print_error("Project name and task ID required")
            return
        try:
            get_task_by_uuid_in_project(args[1], args[2])  # Verify task exists
        except Exception as e:
            print_error(f"Error finding task: {str(e)}")
            return

        delete_task_from_project(get_project_from_name(args[1]), args[2])

        print_info(f"Delete task {args[2]} from project {args[1]}")
    else:
        print_error(f"Unknown resource: {resource}")


def _handle_update_command(args: List[str]) -> None:
    """Handle 'update' commands.
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
            task = get_task_by_uuid_in_project(args[1], args[2])  # Verify task exists
            project = get_project_from_name(args[1])
        except Exception as e:
            print_error(f"Error finding task: {str(e)}")
            return

        print("Please enter new task name [leave blank if want unchanged]:")
        new_name = input().strip()
        print("Please enter new task description [leave blank if want unchanged]:")
        new_description = input().strip()
        print("Please enter new task status (todo, doing, done) [leave blank if want unchanged]:")
        new_status = input().strip()
        print("Please enter new task deadline (YYYY-MM-DD) [leave blank if want unchanged]:")
        new_deadline = input().strip()

        new_task = copy(task)

        try:
            if new_name:
                new_task.set_title(new_name)
            if new_description:
                new_task.set_description(new_description)
            if new_status:
                new_task.set_status(new_status)
            if new_deadline:
                new_task.set_deadline(new_deadline)
        except Exception as e:
            print_error(f"Error updating task: {str(e)}")
            return

        # Update the task in the project
        try:
            update_task_elements(project, args[2], new_task.get_title(), new_task.get_description(), new_task.get_status(), new_task.get_deadline())
        except Exception as e:
            print_error(f"Error saving updated task: {str(e)}")
            return

        print_info(f"Update task {args[2]} in project {args[1]}")

    if resource == "task_status":
        if len(args) < 4:
            print_error("Project name, task ID, and new status required")
            return
        try:
            project = get_project_from_name(args[1])
            task = get_task_by_uuid_in_project(args[1], args[2])  # Verify task exists
            new_status = args[3]
        except Exception as e:
            print_error(f"Error finding task or validating status: {str(e)}")
            return

        try:
            task.set_status(new_status)
            update_task_elements(project, args[2], task.get_title(), task.get_description(), task.get_status(), task.get_deadline())
        except Exception as e:
            print_error(f"Error updating task status: {str(e)}")
            return

        print_info(f"Update task {args[2]} status in project {args[1]} to {new_status}")

    if resource == "project":
        if len(args) < 2:
            print_error("Project name required")
            return
        try:
            project = get_project_from_name(args[1])
        except Exception as e:
            print_error(f"Error finding project: {str(e)}")
            return

        print("Please enter new project name [leave blank if want unchanged]:")
        new_name = input().strip()
        print("Please enter new project description [leave blank if want unchanged]:")
        new_description = input().strip()
        old_name = project.get_name()
        try:
            if new_name:
                project.set_name(new_name)
            if new_description:
                project.set_description(new_description)

            update_project(old_name, project)

        except Exception as e:
            print_error(f"Error updating project: {str(e)}")
            return

        print_info(f"Update project: {args[1]}")

    else:
        print_error(f"Unknown resource: {resource}")


def _handle_get_projects() -> None:
    """
    Retrieve and display all projects.
    """
    try:
        projects = get_project_list()
        if not projects:
            print_info("No projects found")
            return None

        print_success(f"Found {len(projects)} project(s):")
        for idx, project in enumerate(projects, 1):
            print(f"  {idx}. {project.get_name()} - {project.get_description()}")
            tasks = get_project_tasks(project)
            print(f"     Tasks: {len(tasks)}")
            print("     " + "-" * 40)

    except Exception as e:
        print_error(f"Error retrieving projects: {str(e)}")
        return None


def _handle_get_tasks(project_name: str) -> Optional[List]:
    """
    Retrieve and display tasks for a specific project.
    :param project_name: The name of the project to retrieve tasks from.
    :return: List of tasks if successful, None otherwise.
    """
    try:
        project = get_project_from_name(project_name)
        tasks = get_project_tasks(project)

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
    """Print a success message.
    :param message: The success message to print.
    """
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message.
    :param message: The error message to print.
    """
    print(f"✗ Error: {message}")


def print_info(message: str) -> None:
    """Print an informational message.
    :param message: The informational message to print.
    """
    print(f"ℹ {message}")


def print_help() -> None:
    """Display help information about available commands."""
    help_text = """
Todo List CLI - Available Commands:

  get projects                            - List all projects
  get tasks <project>                     - List all tasks in a project
  add project                             - Add a new project
  add task                                - Add a new task to a project
  delete project <name>                   - Delete a project
  delete task <project> <id>              - Delete a task from a project
  update task <proj> <id>                 - Update a task in a project
  update task_status <proj> <id> <status> - Update a task's status
  update project <name>                   - Update a project's name or description
  help                                    - Show this help message
  exit                                    - Exit the CLI
"""
    print(help_text)
