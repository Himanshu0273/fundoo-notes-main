from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import oauth
from app.database import get_db
from app.models.label_model import Label as LabelModel
from app.schemas.label_schema import Label as LabelResponse, LabelBase, UpdateLabel
from app.schemas.user_schema import User
from app.utils.exceptions import LabelNotFoundException

label_router = APIRouter(prefix="/label", tags=["Labels"])


@label_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=LabelResponse
)
def create_label(
    request: LabelBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth.get_current_user),
):
    new_label = LabelModel(label_name=request.label_name, user_id=current_user.id)
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    return new_label


@label_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[LabelResponse]
)
def get_all_label(
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth.get_current_user),
):
    labels = db.query(LabelModel).filter(LabelModel.user_id == current_user.id).all()
    return labels


@label_router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=LabelResponse
)
def update_label(
    id: int,
    request: UpdateLabel,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth.get_current_user),
):
    label_query = db.query(LabelModel).filter(
        LabelModel.id == id, LabelModel.user_id == current_user.id
    )
    label_obj = label_query.first()

    if not label_obj:
        raise LabelNotFoundException(label_id=id)

    updated_label = request.model_dump(exclude_unset=True)
    label_query.update(updated_label)
    db.commit()
    db.refresh(label_obj)

    return label_obj


@label_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_label(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth.get_current_user),
):
    label_query = db.query(LabelModel).filter(
        LabelModel.id == id, LabelModel.user_id == current_user.id
    )
    label_obj = label_query.first()

    if not label_obj:
        raise LabelNotFoundException(label_id=id)

    label_query.delete(synchronize_session=False)
    db.commit()
    return {
        "message": f"The label with id: {id} for user with id: {current_user.id} was deleted!",
        "status": status.HTTP_200_OK,
    }
