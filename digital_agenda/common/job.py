import logging

from django_task.admin import TaskAdmin
from django_task.job import Job


class AsyncTaskAdmin(TaskAdmin):
    class Media:
        css = {"all": ("css/django_task.css",)}
        # Include jquery since that's needed by django_task
        js = (
            "admin/js/vendor/jquery/jquery.min.js",
            "admin/js/jquery.init.js",
            "js/django_task.js",
        )



class LoggingJob(Job):
    parent_logger = logging.getLogger("digital_agenda")

    @classmethod
    def execute(cls, job, task):
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
        handler = logging.StreamHandler(task.log_stream)
        handler.setFormatter(fmt)
        cls.parent_logger.addHandler(handler)

        for task_log_handler in task.get_logger().handlers:
            task_log_handler.setFormatter(fmt)

        try:
            cls.execute_with_logging(job, task)
        finally:
            cls.parent_logger.removeHandler(handler)

    @staticmethod
    def execute_with_logging(job, task):
        raise NotImplemented
