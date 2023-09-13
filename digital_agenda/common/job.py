import logging

from django_task.job import Job


class LoggingJob(Job):
    parent_logger = logging.getLogger("digital_agenda")

    @classmethod
    def execute(cls, job, task):
        task_logger = task.get_logger()
        handler = None
        if task_logger:
            fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
            handler = logging.StreamHandler(task.log_stream)
            handler.setLevel(task_logger.level)
            handler.setFormatter(fmt)
            cls.parent_logger.addHandler(handler)

            for task_log_handler in task.get_logger().handlers:
                task_log_handler.setFormatter(fmt)

        try:
            cls.execute_with_logging(job, task)
        finally:
            if handler:
                cls.parent_logger.removeHandler(handler)

    @staticmethod
    def execute_with_logging(job, task):
        raise NotImplemented
