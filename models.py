from dataclasses import dataclass

@dataclass
class Job:
    title: str
    company: str
    url: str
    source: str
    location: str = ""
    description: str = ""
    easy_apply: bool = False
    score: int = 0