from celery import shared_task


@shared_task
def add(x: int, y: int) -> int:
    return x + y


@shared_task
def test_celery():
    return 'hello world'
