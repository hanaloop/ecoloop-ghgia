import logging
import uuid
import asyncio
import os

logger = logging.getLogger("uvicorn")

class TaskTracker:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TaskTracker, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.running_tasks = {}

    async def add_task(self, task_func, *args, **kwargs):
        task_id = uuid.uuid5(uuid.NAMESPACE_URL, (task_func.__name__))  # Generate a unique UUID for each task
        if task_id in self.running_tasks:
            return False
        task = asyncio.create_task(task_func(*args, **kwargs), name=str(task_id))
        self.running_tasks[task_id] = task
        return task_id

    async def track_tasks(self):
        while True:
            await asyncio.sleep(1)
            # Remove completed or cancelled tasks
            to_remove = [task_id for task_id, task in self.running_tasks.items() if task.done()]
            for task_id in to_remove:
                del self.running_tasks[task_id]
                logger.info(f"Task {task_id} completed or cancelled.")

    def start_tracking(self):
        asyncio.create_task(self.track_tasks())
