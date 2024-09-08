# -*- coding: utf-8 -*-
# @Time        : 2024/7/10
# @Author      : liuboyuan
# @description : https://github.com/josiahcarlson/parse-crontab
import datetime
import math
import threading
import time
from framework.inori_utils.log_utils import LOG


def cal_next_job(trigger_method):
    from crontab import CronTab
    ct = CronTab(trigger_method)
    now = datetime.datetime.utcnow()
    delay = math.ceil(ct.next(now, default_utc=True))
    return delay


class Task:
    def __init__(self, name, cron_expression, func, manual=False, **kwargs):
        self.name = name
        self.trigger_method = cron_expression
        self.func = func
        self.func_kwargs = kwargs
        self.active = True
        self.alive = False
        self.manual = manual
        self.timer = None

    def execute(self):
        """执行任务的函数，并在完成后重新调度"""
        self.alive = True
        try:
            self.func(**self.func_kwargs)
        finally:
            self.alive = False
            if self.active and not self.manual:
                self.reschedule()

    def reschedule(self):
        """重新调度任务"""
        if self.timer:
            self.timer.cancel()
        next_run_time = cal_next_job(self.trigger_method)
        if next_run_time >= 0:
            self.timer = threading.Timer(next_run_time, self.execute)
            self.timer.start()


class ScheduledTaskManager:
    def __init__(self):
        self.tasks = []
        self.running = False
        self.thread = None

    def add_task(self, name, cron_expression, func, manual=False, **kwargs):
        """向任务管理器中添加任务"""
        task = Task(name, cron_expression, func, manual, **kwargs)
        self.tasks.append(task)

    def _run(self):
        """内部使用，用于运行所有已添加的任务"""
        self.running = True
        while self.running:
            for task in self.tasks:
                if task.active and not task.alive and not task.timer:
                    if not task.manual:
                        self.schedule_task(task)
            time.sleep(1)

    def schedule_task(self, task):
        """首次调度一个任务"""
        next_run_time = cal_next_job(task.trigger_method)
        if next_run_time >= 0:
            task.timer = threading.Timer(next_run_time, task.execute)
            task.timer.start()

    def start(self):
        """开始执行所有已添加的任务"""
        if not self.running:
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        """停止所有正在执行的任务和线程"""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
            for task in self.tasks:
                if task.timer:
                    task.timer.cancel()
                    task.timer = None
                    task.alive = False


# 示例使用
def print_task_name(task_name):
    LOG.debug(f"Executing task: {task_name}")


if __name__ == "__main__":
    task_manager = ScheduledTaskManager()
    task_manager.add_task("Task1", "*/5 * * * * * *", print_task_name)
    # task_manager.add_task("Task2", "*/5 * * * * * *", print_task_name, manual=True)
    task_manager.start()
    time.sleep(10)
    task_manager.stop()
    print('=== restart ===')
    task_manager.add_task("Task2", "*/8 * * * * * *", print_task_name)
    task_manager.start()
    time.sleep(24)
    task_manager.stop()
