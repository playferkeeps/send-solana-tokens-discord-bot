from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import base

baseClass = base.Base();

class User(baseClass):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    wallet_address: Mapped["WalletAddress"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class WalletAddress(baseClass):
    __tablename__ = "wallet_address"
    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="wallet_address")
    def __repr__(self) -> str:
        return f"WalletAddress(id={self.id!r}, wallet_address={self.wallet_address!r})"