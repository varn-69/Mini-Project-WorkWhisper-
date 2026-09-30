"""Job source adapters for multi-source job ingestion."""
from .base import BaseJobSource
from .open_jobs_data import OpenJobsDataAdapter
from .adzuna import AdzunaAdapter
from .jooble import JoobleAdapter
from .usajobs import USAJobsAdapter
from .manager import JobSourceManager

__all__ = [
    'BaseJobSource',
    'OpenJobsDataAdapter',
    'AdzunaAdapter',
    'JoobleAdapter',
    'USAJobsAdapter',
    'JobSourceManager',
]
