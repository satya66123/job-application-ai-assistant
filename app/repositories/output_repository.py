from sqlalchemy.orm import Session
from app.models.generated_output import GeneratedOutput


def save_generated_output(
    db: Session,
    user_id: int,
    output_type: str,
    content: str
):
    output = GeneratedOutput(
        user_id=user_id,
        output_type=output_type,
        content=content
    )

    db.add(output)
    db.commit()
    db.refresh(output)

    return output


def get_user_outputs(
    db: Session,
    user_id: int
):
    return db.query(GeneratedOutput).filter(
        GeneratedOutput.user_id == user_id
    ).order_by(
        GeneratedOutput.created_at.desc()
    ).all()