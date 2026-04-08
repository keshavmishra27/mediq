from __future__ import annotations

"""
Bootstrap script to create the first admin user.

Run:
  python -m scripts.create_admin --login-id admin --password "AdminPass123!"
"""

import argparse

from sqlalchemy import select

from app.core.db import SessionLocal
from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.user import User


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--login-id", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--email", default=None)
    parser.add_argument("--phone", default=None)
    args = parser.parse_args()

    db = SessionLocal()
    try:
        existing = db.scalar(select(User).where(User.login_id == args.login_id))
        if existing:
            raise SystemExit(f"User with login_id={args.login_id} already exists")

        u = User(
            role=UserRole.admin,
            login_id=args.login_id,
            email=args.email,
            phone=args.phone,
            password_hash=hash_password(args.password),
            is_active=True,
        )
        db.add(u)
        db.commit()
        print(f"Created admin user: id={u.id} login_id={u.login_id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

