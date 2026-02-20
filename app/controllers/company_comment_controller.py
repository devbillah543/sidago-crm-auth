from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.company import Company
from app.models.company_comment import CompanyComment


class CompanyCommentController:

    # =====================================
    # CREATE COMMENT
    # =====================================
    @staticmethod
    def create_comment(company_id: int, message: str, db: Session, current_user):
        if not message.strip():
            raise ValueError("Comment cannot be empty")

        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValueError("Company not found")

        comment = CompanyComment(
            company_id=company_id,
            user_id=current_user.id if current_user else None,
            comment=message,
            created_at=datetime.utcnow()
        )

        try:
            db.add(comment)
            db.commit()
            db.refresh(comment)
        except Exception as e:
            db.rollback()
            raise e

        return CompanyCommentController._serialize(comment)

    # =====================================
    # GET ALL COMMENTS BY COMPANY ID
    # =====================================
    @staticmethod
    def get_comments_by_company_id(company_id: int, db: Session):
        comments = (
            db.query(CompanyComment)
            .filter(CompanyComment.company_id == company_id)
            .order_by(desc(CompanyComment.id))
            .all()
        )

        return [CompanyCommentController._serialize(c) for c in comments]

    # =====================================
    # GET ALL COMMENTS BY COMPANY NAME
    # =====================================
    @staticmethod
    def get_comments_by_company_name(company_name: str, db: Session):
        company = db.query(Company).filter(Company.name == company_name).first()
        if not company:
            raise ValueError("Company not found")

        return CompanyCommentController.get_comments_by_company_id(company.id, db)

    # =====================================
    # GET SINGLE COMMENT
    # =====================================
    @staticmethod
    def get_comment(comment_id: int, db: Session):
        comment = db.query(CompanyComment).filter(CompanyComment.id == comment_id).first()
        if not comment:
            raise ValueError("Comment not found")

        return CompanyCommentController._serialize(comment)

    # =====================================
    # UPDATE COMMENT
    # =====================================
    @staticmethod
    def update_comment(comment_id: int, message: str, db: Session, current_user):
        if not message.strip():
            raise ValueError("Comment cannot be empty")

        comment = db.query(CompanyComment).filter(CompanyComment.id == comment_id).first()
        if not comment:
            raise ValueError("Comment not found")

        # Only owner can update
        if current_user and comment.user_id != current_user.id:
            raise PermissionError("You are not allowed to update this comment")

        comment.comment = message

        try:
            db.commit()
            db.refresh(comment)
        except Exception as e:
            db.rollback()
            raise e

        return CompanyCommentController._serialize(comment)

    # =====================================
    # DELETE COMMENT
    # =====================================
    @staticmethod
    def delete_comment(comment_id: int, db: Session, current_user):
        comment = db.query(CompanyComment).filter(CompanyComment.id == comment_id).first()
        if not comment:
            raise ValueError("Comment not found")

        # Only owner can delete
        if current_user and comment.user_id != current_user.id:
            raise PermissionError("You are not allowed to delete this comment")

        try:
            db.delete(comment)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

        return {"message": "Comment deleted successfully"}

    # =====================================
    # PRIVATE SERIALIZER
    # =====================================
    @staticmethod
    def _serialize(comment: CompanyComment):
        return {
            "id": comment.id,
            "company_id": comment.company_id,
            "message": comment.comment,
            "created_at": comment.created_at,
            "user": {
                "id": comment.user.id if comment.user else None,
                "name": comment.user.username if comment.user else "Unknown"
            }
        }