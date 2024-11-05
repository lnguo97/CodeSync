from typing import List
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Report(Base):
    __tablename__ = "report"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    owner: Mapped[str]

    parameters: Mapped[List["ReportParameter"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )
    queries: Mapped[List["Query"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )
    outputs: Mapped[List["Output"]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )


class Query(Base):
    __tablename__ = "query"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    sql: Mapped[str]

    output_id: Mapped[int] = mapped_column(ForeignKey("output.id"))
    output: Mapped["Output"] = relationship()

    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"))
    report: Mapped["Report"] = relationship(back_populates="queries")

    parameters: Mapped[List["QueryParameter"]] = relationship(
        back_populates="query", cascade="all, delete-orphan"
    )


class Output(Base):
    __tablename__ = "output"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str]

    template_id: Mapped[int] = mapped_column(ForeignKey("template.id"))
    template: Mapped["Template"] = relationship()

    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"))
    report: Mapped["Report"] = relationship(back_populates="outputs")


class Template(Base):
    __tablename__ = "template"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    file_path: Mapped[str]
    meta_data: Mapped[str]


class ReportParameter(Base):
    __tablename__ = "report_parameter"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    dtype: Mapped[str]
    value: Mapped[str]

    report_id: Mapped[int] = mapped_column(ForeignKey("report.id"))
    report: Mapped["Report"] = relationship(back_populates="parameters")


class QueryParameter(Base):
    __tablename__ = "query_parameter"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    dtype: Mapped[str]
    value: Mapped[str]

    query_id: Mapped[int] = mapped_column(ForeignKey("query.id"))
    query: Mapped["Query"] = relationship(back_populates="parameters")


if __name__ == '__main__':
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
