from __future__ import annotations
from typing import Iterable, List, Tuple, Optional
from difflib import SequenceMatcher
import json

from app.models import JobPosting, User


def _tokenize(text: Optional[str]) -> List[str]:
    if not text:
        return []
    return [t for t in ''.join(c.lower() if c.isalnum() else ' ' for c in text).split() if t]


def _jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def score_jobs_for_user(user: Optional[User], jobs: Iterable[JobPosting]) -> List[Tuple[JobPosting, Optional[float]]]:
    if not user:
        return [(j, None) for j in jobs]

    resume_tokens = _tokenize(user.resume_text or '')
    try:
        skills_list = json.loads(user.resume_skills or '[]')
    except Exception:
        skills_list = []
    skills_tokens = [s.lower() for s in skills_list if isinstance(s, str)]

    combined = set(resume_tokens) | set(skills_tokens)

    results: List[Tuple[JobPosting, Optional[float]]] = []
    for job in jobs:
        job_tokens = _tokenize((job.title or '') + ' ' + (job.description or ''))
        jacc = _jaccard(list(combined), job_tokens)
        results.append((job, round(jacc, 4)))
    return results
