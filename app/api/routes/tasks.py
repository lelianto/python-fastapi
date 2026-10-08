"""HTTP endpoints for task CRUD operations."""

from fastapi import APIRouter, HTTPException, Query, Response, status
from app.api.dependencies import TaskServiceDependency
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task import TaskNotFoundError

router = APIRouter(prefix="/tasks", tags=["tasks"])


def not_found(error: TaskNotFoundError) -> HTTPException:
    """Translate a domain error into an HTTP response."""
    return HTTPException(status_code=404, detail=str(error))


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, service: TaskServiceDependency) -> TaskRead:
    """Create and return a new task."""
    return service.create(payload)


@router.get("", response_model=list[TaskRead])
def list_tasks(service: TaskServiceDependency, offset: int = Query(0, ge=0),
               limit: int = Query(20, ge=1, le=100)) -> list[TaskRead]:
    """Return tasks in stable ID order, with offset/limit pagination."""
    return service.list(offset=offset, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, service: TaskServiceDependency) -> TaskRead:
    """Return one task by its numeric ID."""
    try:
        return service.get(task_id)
    except TaskNotFoundError as error:
        raise not_found(error) from error


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate,
                service: TaskServiceDependency) -> TaskRead:
    """Update only the fields included in the request body."""
    try:
        return service.update(task_id, payload)
    except TaskNotFoundError as error:
        raise not_found(error) from error


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, service: TaskServiceDependency) -> Response:
    """Delete one task and return an empty success response."""
    try:
        service.delete(task_id)
    except TaskNotFoundError as error:
        raise not_found(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
