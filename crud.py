from models import User, JobApplication


def create_user(db, user):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()


def create_job_application(db, application):
    db_app = JobApplication(**application.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def get_user_applications(db, user_id):
    return db.query(JobApplication).filter(JobApplication.user_id == user_id).all()


def update_job_application(db, app_id, updates):
    db_app = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if db_app:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(db_app, key, value)
        db.commit()
        db.refresh(db_app)
    return db_app
