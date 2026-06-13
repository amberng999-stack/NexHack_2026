from __future__ import annotations

import re
from dataclasses import dataclass

from app.models import ClauseFinding, RiskLevel


@dataclass(frozen=True)
class RiskRule:
    id: str
    category: str
    title: str
    severity: RiskLevel
    patterns: tuple[str, ...]
    explanation: str
    recommendation: str


RISK_RULES: tuple[RiskRule, ...] = (
    RiskRule(
        id="auto-renewal",
        category="Term and termination",
        title="Automatic renewal or silent extension",
        severity="high",
        patterns=(
            r"automatic(?:ally)? renew",
            r"auto[-\s]?renew",
            r"unless .* written notice .* (?:30|60|90) days",
            r"renewal term",
            r"successive terms?",
            r"failure to give notice .* renew",
        ),
        explanation="The agreement may renew without an active approval step.",
        recommendation="Require clear renewal notice, approval workflow, and easy opt-out before renewal.",
    ),
    RiskRule(
        id="unilateral-change",
        category="Change control",
        title="Unilateral modification right",
        severity="critical",
        patterns=(
            r"sole discretion",
            r"may modify .* at any time",
            r"without prior notice",
            r"unilateral(?:ly)? (?:modify|change|amend)",
            r"right to change .* terms",
            r"at its discretion",
        ),
        explanation="One party may change important terms without negotiation or notice.",
        recommendation="Require written notice, mutual consent, and a right to terminate if material terms change.",
    ),
    RiskRule(
        id="hidden-fees",
        category="Fees and payment",
        title="Potential hidden fees or pass-through charges",
        severity="high",
        patterns=(
            r"additional fees?",
            r"administrative charges?",
            r"pass[-\s]?through costs?",
            r"fees .* subject to change",
            r"extra charges?",
            r"separate charges?",
            r"pricing .* may be adjusted",
        ),
        explanation="The contract may allow extra charges beyond the headline price.",
        recommendation="List all charge categories, caps, approval requirements, and invoice dispute rights.",
    ),
    RiskRule(
        id="broad-liability-waiver",
        category="Liability",
        title="Broad limitation or waiver of liability",
        severity="critical",
        patterns=(
            r"not liable for .* indirect",
            r"limitation of liability",
            r"liability .* capped",
            r"waive .* damages",
            r"exclude .* damages",
            r"disclaim .* liability",
            r"consequential damages",
        ),
        explanation="Liability may be excluded or capped too broadly for enterprise risk tolerance.",
        recommendation="Carve out fraud, confidentiality, data breach, IP infringement, and gross negligence.",
    ),
    RiskRule(
        id="data-use",
        category="Data and privacy",
        title="Broad data use or transfer permission",
        severity="high",
        patterns=(
            r"use .* data .* improve",
            r"share .* data .* affiliates?",
            r"transfer .* personal data",
            r"process .* data .* analytics",
            r"data .* third parties",
            r"personal information .* affiliates?",
        ),
        explanation="The vendor may use, share, or transfer enterprise/customer data broadly.",