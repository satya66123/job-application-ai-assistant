from sqlalchemy.orm import Session
from app.models.ats_report import ATSReport


def save_ats_report(
    db: Session,
    user_id: int,
    resume_text: str,
    job_description: str,
    match_score: str,
    report: str
):
    ats = ATSReport(
        user_id=user_id,
        resume_text=resume_text,
        job_description=job_description,
        match_score=match_score,
        report=report
    )

    db.add(ats)
    db.commit()
    db.refresh(ats)

    return ats


def get_user_ats_reports(
    db: Session,
    user_id: int
):
    return db.query(ATSReport).filter(
        ATSReport.user_id == user_id
    ).order_by(
        ATSReport.created_at.desc()
    ).all()