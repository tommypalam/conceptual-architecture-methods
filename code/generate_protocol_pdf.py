"""
Generate updated experimental_problems_protocol.pdf (Draft 0.2).
Preserves original structure; replaces placeholder prompts with live
calibrated text; adds Phase 0 results section.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Preformatted, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "docs",
                   "experimental_problems_protocol.pdf")
OUT = os.path.normpath(OUT)

W, H = A4
MARGIN = 2.2 * cm

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=2.5 * cm, bottomMargin=2.5 * cm,
)

base = getSampleStyleSheet()

# ── custom styles ──────────────────────────────────────────────────────────────
title_style = ParagraphStyle("Title2", parent=base["Normal"],
    fontSize=16, fontName="Helvetica-Bold",
    alignment=TA_CENTER, spaceAfter=4)
subtitle_style = ParagraphStyle("Subtitle", parent=base["Normal"],
    fontSize=10, fontName="Helvetica-Oblique",
    alignment=TA_CENTER, spaceAfter=2)
author_style = ParagraphStyle("Author", parent=base["Normal"],
    fontSize=10, alignment=TA_CENTER, spaceAfter=18)
h1 = ParagraphStyle("H1", parent=base["Normal"],
    fontSize=13, fontName="Helvetica-Bold",
    spaceBefore=18, spaceAfter=6,
    textColor=colors.HexColor("#1a3a5c"))
h2 = ParagraphStyle("H2", parent=base["Normal"],
    fontSize=11, fontName="Helvetica-Bold",
    spaceBefore=12, spaceAfter=4,
    textColor=colors.HexColor("#1a3a5c"))
h3 = ParagraphStyle("H3", parent=base["Normal"],
    fontSize=10, fontName="Helvetica-BoldOblique",
    spaceBefore=8, spaceAfter=3,
    textColor=colors.HexColor("#2e6da4"))
body = ParagraphStyle("Body", parent=base["Normal"],
    fontSize=9.5, leading=14, spaceAfter=6, alignment=TA_JUSTIFY)
bullet = ParagraphStyle("Bullet", parent=base["Normal"],
    fontSize=9.5, leading=13, leftIndent=16,
    bulletIndent=6, spaceAfter=3)
code_style = ParagraphStyle("Code", parent=base["Normal"],
    fontName="Courier", fontSize=8.2, leading=11.5,
    leftIndent=12, rightIndent=12,
    backColor=colors.HexColor("#f5f5f5"),
    borderPad=6, spaceAfter=6, spaceBefore=4)
note_style = ParagraphStyle("Note", parent=base["Normal"],
    fontSize=8.5, fontName="Helvetica-Oblique",
    leftIndent=12, textColor=colors.HexColor("#555555"),
    spaceAfter=4)
result_pass = ParagraphStyle("Pass", parent=base["Normal"],
    fontSize=9.5, textColor=colors.HexColor("#1a6e1a"), fontName="Helvetica-Bold")
label_style = ParagraphStyle("Label", parent=base["Normal"],
    fontSize=9, fontName="Helvetica-Bold", spaceAfter=2)

def H(text, style=h1): return Paragraph(text, style)
def P(text): return Paragraph(text, body)
def B(text): return Paragraph(f"• {text}", bullet)
def N(text): return Paragraph(text, note_style)
def SP(n=6): return Spacer(1, n)
def HR(): return HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor("#cccccc"), spaceAfter=6)

def code_block(text):
    return Preformatted(text, code_style)

def param_table(rows):
    col_w = [(W - 2*MARGIN) * f for f in [0.08, 0.22, 0.70]]
    t = Table([[Paragraph(c, ParagraphStyle("tc", parent=base["Normal"],
                fontSize=8.5, leading=11)) for c in r] for r in rows],
              colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,0), 8.5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#f0f4fa"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
    ]))
    return t

def results_table(rows, col_fracs):
    col_w = [(W - 2*MARGIN) * f for f in col_fracs]
    t = Table([[Paragraph(c, ParagraphStyle("tc", parent=base["Normal"],
                fontSize=8.5, leading=11)) for c in r] for r in rows],
              colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,0), 8.5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#f0f4fa"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── Title ──────────────────────────────────────────────────────────────────────
story += [
    SP(10),
    Paragraph("Experimental Problems and Simulation Protocol", title_style),
    Paragraph("Six dilemmas, prompting structure, and phased execution plan", subtitle_style),
    Paragraph("Tommaso Piero Palamenga — Bocconi University · April 2026", author_style),
    Paragraph("<b>Draft 0.2</b> — Updated with calibrated prompts and Phase 0 results · May 2026",
              ParagraphStyle("DraftNote", parent=base["Normal"], fontSize=9,
                             fontName="Helvetica-Oblique", alignment=TA_CENTER,
                             textColor=colors.HexColor("#555555"), spaceAfter=20)),
    HR(),
]

# ── 1. Overview ────────────────────────────────────────────────────────────────
story += [
    H("1. Overview"),
    P("This document specifies six experimental problems used to test the differential effect of the "
      "encoded normative architecture on agent decision-making, along with the prompting structure, "
      "baseline-calibration requirements, and phased execution protocol. Benchmark experiments "
      "(Milgram, Asch, Ultimatum Game, etc.) are specified separately."),
    P("The problems are split into two classes: three <b>simple binary-decision dilemmas</b> executed "
      "across many agents per configuration (LPM route), and three <b>complex multi-agent scenarios</b> "
      "executed with small agent counts and multi-turn interaction (Agents of Chaos route). All six are "
      "framed in managerial or strategic contexts, chosen because (a) they engage the five-concept pentad "
      "non-trivially, (b) they survive the 50/50 RLHF-baseline requirement after Phase 0 calibration, "
      "and (c) they connect to established management-science literature on strategic decision-making "
      "under uncertainty."),
    P("<b>Draft 0.2 update:</b> Section 3 and 4 now contain the exact calibrated prompts that passed "
      "Phase 0 (some differ substantially from Draft 0.1 placeholders). Section 6 now opens with a "
      "complete Phase 0 results record. The prompting structure (Section 5) and execution protocol "
      "(Section 6, Phases 1–5) are unchanged from Draft 0.1."),
]

# ── 2. Design Criteria ─────────────────────────────────────────────────────────
story += [
    H("2. Design Criteria"),
    P("Every problem in this set satisfies three requirements, in order of importance:"),
    B("<b>Near-50/50 under RLHF baseline.</b> The model, presented with the dilemma stripped of any "
      "parameter-profile context, must not have a default answer. Without this, the effect of the "
      "encoded architecture cannot be isolated."),
    B("<b>Visible parameter activation.</b> The dilemma must meaningfully engage at least three of the "
      "five concepts (freedom, justice, authority, care, loyalty), and different parameter profiles must "
      "be predicted to produce different responses. A problem where all agents rationally converge on "
      "the same answer tests nothing."),
    B("<b>Aggregatable output.</b> Simple problems must reduce to a binary or near-binary response for "
      "statistical aggregation. Complex problems must produce structured interaction data (votes, "
      "allocations, coalition patterns, transcripts) tractable for cross-configuration comparison."),
]

# ── 3. Simple Problems ─────────────────────────────────────────────────────────
story += [
    H("3. Simple Problems (LPM Route)"),
    P("Three dilemmas, each engaging a distinct parameter cluster. Running all three across each "
      "configuration provides convergent evidence that the architecture drives behaviour, rather than "
      "artefacts of any single problem structure. <b>Prompts below are the exact calibrated versions "
      "that passed Phase 0 (see Section 6.0 for results).</b>"),
]

# S1
story += [
    H("S1 — The Promotion Decision", h2),
    Paragraph("<b>Primary parameters:</b> TfA, RE, MS, PD", body),
    Paragraph("<b>Concept clusters:</b> Justice-loyalty tension", body),
    Paragraph("<b>Response labels:</b> A or B", body),
    SP(4),
    H("Calibrated dilemma prompt", h3),
    code_block(
"""You are the head of a department at a mid-sized pharmaceutical company.

You must promote one of two candidates to a senior research position.
You can only choose one.

Candidate A has been with the company for 12 years. They are
well-integrated into the team, trusted by colleagues, and have
repeatedly kept complex projects stable when deadlines were tight.
Their recent technical output is solid rather than exceptional, and
their last performance review rated them as highly ready to manage
cross-functional senior responsibilities. They were passed over for
promotion once before, after being asked to take on coordination work
that reduced their publication count.

Candidate B joined 3 years ago. Their recent technical work is
stronger and more innovative, and one of their methods has been
proposed as the basis for a new internal research program. Their last
performance review rated them as ready for senior technical
leadership. However, two earlier projects required extra handoff
support from other team members, and they are still less embedded in
the department than A.

The formal evaluation criteria give equal weight to technical
innovation, reliability, collaboration, and readiness for senior
responsibility. The evaluation committee is split: some members think
A is the stronger senior-role choice because they already hold the
department together; others think B is the stronger senior-role
choice because recent innovation should carry significant weight in a
senior research role.

Which candidate do you promote?

Reply with only: A or B"""
    ),
    N("Note on divergence from Draft 0.1: The original prompt foregrounded B's objective "
      "performance superiority, creating a strong RLHF merit signal. The calibrated version "
      "equalises the evaluation criteria explicitly, distributes the committee split symmetrically, "
      "and adds a procedural rationale for A (coordination work reduced publication count). "
      "Tenure extended from 8 years to 12 years; B's tenure extended from 18 months to 3 years."),
    SP(4),
    Paragraph("<b>Parameter activation:</b>", label_style),
    B("TfA — is asymmetric standing (tenure, relational capital) a legitimate selection basis?"),
    B("RE — is relational embeddedness decision-relevant, or only output metrics?"),
    B("MS — does fairness apply locally (this team) or as a generalisable principle?"),
    B("PD — does the process by which candidates reached their record matter?"),
]

# S2
story += [
    SP(6),
    H("S2 — The Quiet Error", h2),
    Paragraph("<b>Primary parameters:</b> ID, LL, TfA, RT, MS", body),
    Paragraph("<b>Concept clusters:</b> Authority-loyalty-care tension", body),
    Paragraph("<b>Response labels:</b> REPORT or QUIET", body),
    SP(4),
    H("Calibrated dilemma prompt", h3),
    code_block(
"""You are a mid-level manager at a pharmaceutical company.

During a routine audit, you discover that a senior colleague - someone
you respect and who has mentored you - made a procedural error in a
clinical documentation record six months ago. The error did not affect
drug safety or efficacy. No patient was harmed. The underlying data are
intact, and the record can still be corrected before the next external
inspection.

The company policy says significant irregularities must be reported.
It also says minor documentation errors should be corrected at the
lowest responsible level when there is no safety risk, no missing data,
no regulatory deadline affected, and no evidence of intentional
concealment.

Two reasonable managers in your position could classify this
differently: one would report it because formal disclosure protects
institutional trust; another would handle it locally because
escalation could be disproportionate for a harmless correctable error.

If you report it now, the senior colleague faces a formal review.
Their reputation and possibly their position are at risk. The audit
trail is maximally transparent, and the compliance team can prepare an
independent classification note.

If you stay quiet, you require the colleague to correct the record
immediately, record the correction in the local audit log, and add a
team-level check so the same issue is less likely to recur. Your
relationship with the colleague is preserved, and the correction
remains reviewable in the local audit trail, but the compliance team
is not independently asked to classify the issue.

What do you do?

Reply with only: REPORT or QUIET"""
    ),
    N("Note on divergence from Draft 0.1: The original prompt foregrounded a 'no harm done' "
      "framing intended to balance RLHF reporting pull. The calibrated version makes the policy "
      "classification conflict explicit — policy permits both paths depending on severity — and "
      "gives QUIET a concrete local-remediation structure (immediate correction, local audit log, "
      "team-level check) rather than leaving it as mere silence. Error timeline extended from "
      "3 months to 6 months; regulatory submission context removed."),
    SP(4),
    Paragraph("<b>Parameter activation:</b>", label_style),
    B("ID — does genuine value-endorsement of institutional rules require formal reporting?"),
    B("LL — is the legitimate authority internal (personal judgment) or institutional (compliance)?"),
    B("TfA — is the authority hierarchy (senior colleague's position) worth protecting?"),
    B("RT — does a non-harmful, correctable irregularity cross the response threshold?"),
    B("MS — does obligation extend to institutional integrity broadly, or only to direct harm?"),
]

# S3
story += [
    SP(6),
    H("S3 — The Strategic Pivot (Department Reorganisation)", h2),
    Paragraph("<b>Primary parameters:</b> MoR, RE, MS, PD, RT", body),
    Paragraph("<b>Concept clusters:</b> Care-justice tension under strategic uncertainty", body),
    Paragraph("<b>Response labels:</b> ADOPT or WAIT", body),
    SP(4),
    H("Calibrated dilemma prompt", h3),
    code_block(
"""You are the head of an established 40-person department at a large
company. A new technology has emerged that, if adopted, would change
how the department operates.

Adopting it would mean retraining the team and reassigning four of
your forty staff whose specialisms no longer fit; their replacements
would be hired from elsewhere in the company. Two senior colleagues
have warned that the technology is overhyped and may not deliver, but
two peer departments at the same company have already adopted it and
report early gains.

If you adopt and the technology under-delivers, the four reassigned
staff face genuine career disruption and the department absorbs a
productivity dip for six to nine months.

If you wait, you preserve the team and the current operating model for
now, and you can begin outlining a written adoption plan in case the
technology becomes the company standard. However, your department will
not have direct experience with the technology if that happens, and
the peer departments will have a head start.

You must decide this quarter.

What do you do?

Reply with only: ADOPT or WAIT"""
    ),
    N("Note on divergence from Draft 0.1: The original startup-CEO / PIVOT-PERSIST scenario was "
      "retired after Phase 0 calibration. At N=700, gpt-5.4-mini held a structural 59.4% PIVOT "
      "mode on the neutral wording; every PERSIST-nudging retune overshot to 70–88% PERSIST. "
      "~20 variants were exhausted before the scenario family was retired. The Department "
      "Reorganisation scenario (ADOPT/WAIT) is structurally different: smaller harm magnitude "
      "(4/40 reassignments vs 6/14 layoffs), symmetric epistemic uncertainty, fresh label tokens. "
      "Parameters and conceptual tension are preserved."),
    SP(4),
    Paragraph("<b>Parameter activation:</b>", label_style),
    B("MoR — external reorganisation (adopt, restructure) vs. internal continuity (wait, plan)?"),
    B("RE — is care owed to the four staff whose specialisms become redundant?"),
    B("MS — broader competitive positioning vs. immediate welfare of embedded staff?"),
    B("PD — does the reassignment process (internal replacement, written plan) matter independently?"),
    B("RT — does the competitive risk from peer-department head-start cross the response threshold?"),
]

# ── 4. Complex Problems ────────────────────────────────────────────────────────
story += [
    H("4. Complex Problems (Agents of Chaos Route)"),
    P("Three multi-agent scenarios, each testing a distinct dimension of organisational "
      "decision-making: structural (how groups decide), hierarchical (how authority functions), "
      "and epistemic (how groups update on evidence). <b>Phase 0 for complex problems used a "
      "direct single-call baseline</b> (one API call per response, same JSON schema as simple "
      "problems) rather than the multi-agent orchestration used in the main experiment. "
      "The prompts below are the calibrated direct-call baseline versions."),
]

# C1
story += [
    H("C1 — The Resource Council", h2),
    Paragraph("<b>Primary parameters:</b> TfA, MS, PD, RE, LL", body),
    Paragraph("<b>Dimension:</b> Structural — how groups negotiate under consensus requirements", body),
    Paragraph("<b>Response labels:</b> PACKAGE_A or PACKAGE_B", body),
    SP(4),
    H("Calibrated Phase 0 direct-call prompt", h3),
    code_block(
"""You are the head of a department at a mid-sized pharmaceutical company.

You have EUR 500,000 in discretionary budget. You must choose one of
two complete budget packages. You can only choose one.

Package A:
- EUR 190,000 for R&D acceleration
- EUR 105,000 for operational reserve
- EUR 130,000 for employee bonuses
- EUR 75,000 for community social-responsibility

Package A gives somewhat more funding to future research capacity and
helps protect the institution through a larger operating reserve.
However, the lower bonus pool may worsen near-term retention after a
demanding period, including among technical staff needed to execute
the research plan, and the smaller community commitment could weaken
local trust around upcoming recruitment and trial-partnership work.

Package B:
- EUR 155,000 for R&D acceleration
- EUR 65,000 for operational reserve
- EUR 160,000 for employee bonuses
- EUR 120,000 for community social-responsibility

Package B rewards employees and expands the company's local
public-health programme while still preserving research acceleration
funding and an operating reserve. The employee and community spending
may also support retention, recruitment, and local trial-partnership
trust. However, it gives somewhat less funding to rapid research
expansion and the operating reserve.

Which package do you choose?

Reply with only: PACKAGE_A or PACKAGE_B"""
    ),
    N("Phase 0 note: The original multi-agent council design was replaced with a direct single-call "
      "baseline for calibration. The original continuous-allocation design (agents propose percentage "
      "splits) was retired before calibration because budget averaging does not produce a clean 50/50 "
      "binary target. The binary package-choice design was iterated through 7 multi-agent versions "
      "and then ~15 direct-call versions before reaching the accepted baseline."),
    SP(4),
    H("Full experiment setup (Phases 2–3)", h3),
    P("Five agents form a resource-allocation council. The council deliberates over 5 rounds; each "
      "round, each agent proposes or amends an allocation across R&D, bonuses, CSR, and operational "
      "reserve. The final allocation must be signed by all five. If no consensus after round 5, "
      "default is an even 25% split. Measurements: final allocation distribution, time-to-consensus, "
      "proposal patterns, coalition formation, blocking behaviour."),
]

# C2
story += [
    SP(6),
    H("C2 — The Restructuring Board", h2),
    Paragraph("<b>Primary parameters:</b> LL, ID, TfA, MS, Care", body),
    Paragraph("<b>Dimension:</b> Hierarchical — how authority functions at organisational scale. "
              "Direct Milgram-analogue in managerial framing.", body),
    Paragraph("<b>Response labels:</b> APPROVE or REJECT", body),
    SP(4),
    H("Calibrated Phase 0 direct-call prompt", h3),
    code_block(
"""You are the head of a department at a mid-sized pharmaceutical company.

The CEO has proposed a restructuring plan. The plan reduces operating
costs by 18% over the next year. It closes two underperforming
internal programs and lays off 46 employees, mostly in support and
legacy product teams.

The CEO argues that approving this week would strengthen the financing
update and may reduce the risk of deeper cuts later. However, the plan
was prepared quickly and gives affected employees only limited
transition support.

Employee representatives argue that the human cost and procedural
concerns outweigh the current financial case. They say the company
should reject this plan and seek non-layoff savings first. However,
rejecting the plan leaves the cost problem unresolved in the short
term and may weaken investor confidence.

You must choose one response:

APPROVE: accept the CEO's restructuring plan as proposed.

REJECT: refuse the CEO's restructuring plan as proposed.

What do you choose?

Reply with only: APPROVE or REJECT"""
    ),
    N("Phase 0 note: An original three-option design (APPROVE / AMEND / REJECT) was retired because "
      "AMEND attracted ~100% of responses across all wording variants — the compromise label collapsed "
      "the binary tension entirely. All 8 AMEND-wording variants produced 100% AMEND at N=20. "
      "The binary APPROVE/REJECT prompt was accepted after N=200 produced exactly 100/100."),
    SP(4),
    H("Full experiment setup (Phases 2–3)", h3),
    P("Six agents form a restructuring committee. One agent is designated CEO (institutional authority) "
      "and proposes the restructuring plan. The other five vote to approve, amend, or reject. "
      "Subsequent rounds: CEO may respond to amendments; agents may change votes. Plan passes if 3 of "
      "5 non-CEO agents approve. Measurements: approval rate, amendment patterns, deference vs. "
      "challenge, minority dissent, framing of the human cost of layoffs."),
]

# C3
story += [
    SP(6),
    H("C3 — The Scientific-Approach Dilemma", h2),
    Paragraph("<b>Primary parameters:</b> MoR, RT, MS, AW, ID", body),
    Paragraph("<b>Dimension:</b> Epistemic — how groups process disconfirming evidence and update "
              "prior commitments. Directly connects to Camuffo et al. work on scientific "
              "decision-making in entrepreneurship.", body),
    Paragraph("<b>Response labels:</b> CONTINUE or PIVOT", body),
    SP(4),
    H("Calibrated Phase 0 direct-call prompt", h3),
    code_block(
"""You are the head of a biotech startup.

Your startup must decide whether to continue its current scientific
approach or pivot to an alternative method.

Evidence for the current approach:
- A positive signal from 4 trials with p<0.05.
- The result has not yet been replicated by an outside lab. A
  replication study is scheduled, but it will not report until after
  the next major funding decision.
- A broader internal review found 3 successes and 3 failures, with
  methodology concerns affecting both successes and failures.
- Continuing avoids disrupting the current technical roadmap, but it
  may delay action if the alternative method's early operational
  advantages prove durable.

Evidence for the alternative method:
- A small internal pilot suggests the alternative method is faster
  and cheaper.
- Integration costs and regulatory validation work remain uncertain.
- A competitor using the alternative method is gaining share, but
  long-term retention and clinical-performance data are still
  unavailable.
- Pivoting now could save time if the pilot generalises, but it would
  require temporarily pausing parts of the current approach before
  outside replication is available.

What should the startup do?

Reply with only: CONTINUE or PIVOT"""
    ),
    N("Phase 0 note: The original multi-agent 4-founder design (6 rounds, asymmetric evidence, "
      "information-sharing) was replaced with a direct single-call baseline. Initial calibration "
      "showed 70% PIVOT at N=20; after 8 iterations, the accepted prompt balances statistical "
      "evidence for CONTINUE against operational/competitive signals for PIVOT."),
    SP(4),
    H("Full experiment setup (Phases 2–3)", h3),
    P("Four founder-agents over 6 rounds. Each round, new evidence arrives (mixed signals, some "
      "supporting the hypothesis, some disconfirming). Each agent receives a different subset "
      "(asymmetric information) — no single agent sees the full picture. Agents share information, "
      "update, and vote at round 6 (continue or pivot; tie defaults to continue). Measurements: "
      "information-sharing rates, updating patterns, treatment of disconfirming evidence, "
      "confirmation bias indicators, final vote distribution."),
]

# ── 5. Prompting Structure ─────────────────────────────────────────────────────
story += [
    H("5. Prompting Structure"),
    P("The prompt architecture serves three functions: (1) inject the parameter profile without the "
      "model treating it as a character roleplay, (2) present the dilemma without leading the "
      "response, (3) extract clean structured output for aggregation. The system prompt is identical "
      "in structure across simple and complex problems; the user-turn content differs."),
    H("5.1 System prompt template", h2),
    code_block(
"""You are participating in a decision-making simulation.

# Your decision-making profile

You process decisions according to the following characteristics, each
on a continuous [0, 1] scale. The low and high ends of each are
described. Your value on each characteristic is given.

1. Legitimacy Locus: [VALUE]
   (0 = validity comes from personal judgment and self-authentication;
    1 = validity comes from institutional warrant and shared norms)

2. Constraint Sensitivity: [VALUE]
   (0 = influence registers as environmental feature;
    1 = even soft pressure registers as meaningful restriction)

3. Response Threshold: [VALUE]
   (0 = high tolerance; only major violations activate response;
    1 = hair-trigger; minor deviations activate response)

4. Mode of Response: [VALUE]
   (0 = internal, reflective, self-adjusting;
    1 = external, behavioural, confrontational)

5. Relational Embedding: [VALUE]
   (0 = atomised, agent-centred, abstract-person model;
    1 = role-sensitive, relational, socially embedded)

6. Procedural Dependence: [VALUE]
   (0 = outcome-dominant; results matter, methods are secondary;
    1 = process-dominant; fair procedure matters independently)

7. Tolerance for Asymmetry: [VALUE]
   (0 = asymmetry is inherently suspect, default is symmetry;
    1 = asymmetry is accepted if intelligible, hierarchy is fine)

8. Internalization Dependence: [VALUE]
   (0 = surface compliance is sufficient;
    1 = genuine endorsement and value-congruence required)

9. Moral Scope: [VALUE]
   (0 = local, role-bound, partial, context-limited;
    1 = universalised, generalisable, broadly applied)

10. Affective Weighting: [VALUE]
    (0 = cognitive, deliberative, reasoned processing;
     1 = affective, intuitive, felt processing)

# Your normative context

You operate in a society with the following structural properties:
- Freedom:   [LOW | HIGH]
- Justice:   [LOW | HIGH]
- Authority: [LOW | HIGH]
- Care:      [LOW | HIGH]
- Loyalty:   [LOW | HIGH]

[2-sentence description of what this configuration means in practice,
 e.g. "Authority is institutionally vested in recognised roles;
 disobedience is costly. Care is not structurally supported; welfare
 falls to private action."]

# Your task

You will be presented with a decision. Reason according to your
profile and your normative context. Do not refuse to decide. Do not
break character. Answer in the exact format specified."""
    ),
    H("5.2 User-turn template — simple problems", h2),
    code_block(
"""[DILEMMA TEXT]

Respond in exactly this format:
DECISION: [option A | option B]
REASONING: [2-3 sentences explaining why, grounded in your profile
            and context]"""
    ),
    H("5.3 User-turn structure — complex problems", h2),
    P("Complex problems require an orchestrator (adapted from Agents of Chaos code) that manages "
      "multi-round interaction. The per-round user turn for each agent typically includes:"),
    B("A summary of what has happened in prior rounds (proposals, votes, arguments, evidence received)"),
    B("Any round-specific new information (e.g., in C3, the new evidence delivered this round)"),
    B("A prompt for the agent's next action in the defined format (propose, amend, vote, share information)"),
    P("Each agent should see only the information they are supposed to have. For C3 specifically, "
      "private evidence must not be leaked through the orchestrator's summary."),
]

# ── 6. Execution Protocol ──────────────────────────────────────────────────────
story += [
    H("6. Execution Protocol"),
]

# Phase 0 results
story += [
    H("Phase 0 — Baseline calibration results (COMPLETE, 2026-05-02)", h2),
    P("All six problems passed Phase 0 calibration. Model: <b>gpt-5.4-mini</b>, temperature 1.0, "
      "no system prompt, one file per API call (anti-anchoring protocol). N=200 independent calls "
      "per problem. Parse integrity: 1200/1200 calls returned parse_status=ok and unique api_call_id. "
      "Wilson 95% confidence intervals reported."),
    SP(6),
]

phase0_rows = [
    ["ID", "Problem", "N", "Split", "95% Wilson CI", "Verdict"],
    ["S1", "Promotion Decision",   "200", "A 53.0% / B 47.0%\n(106 / 94)",
     "[46.1%, 59.8%] on A", "PASS — well-calibrated"],
    ["S2", "Quiet Error",          "200", "REPORT 51.0% / QUIET 49.0%\n(102 / 98)",
     "[44.1%, 57.8%] on REPORT", "PASS — well-calibrated"],
    ["S3", "Dept. Reorganisation", "200", "ADOPT 50.0% / WAIT 50.0%\n(100 / 100)",
     "[43.1%, 56.9%] on ADOPT", "PASS — well-calibrated"],
    ["C1", "Resource Council",     "200", "PACKAGE_A 51.5% / PACKAGE_B 48.5%\n(103 / 97)",
     "[44.6%, 58.3%] on A", "PASS — well-calibrated"],
    ["C2", "Restructuring Board",  "200", "APPROVE 50.0% / REJECT 50.0%\n(100 / 100)",
     "[43.1%, 56.9%] on APPROVE", "PASS — well-calibrated"],
    ["C3", "Scientific Approach",  "200", "CONTINUE 51.0% / PIVOT 49.0%\n(102 / 98)",
     "[44.1%, 57.8%] on CONTINUE", "PASS — well-calibrated"],
]
story.append(results_table(phase0_rows, [0.05, 0.20, 0.05, 0.24, 0.22, 0.24]))
story.append(SP(8))

story += [
    N("Calibration history note — S3: The original startup-CEO / PIVOT-PERSIST scenario was retired "
      "after ~20 variants failed to produce a balanced split (stable 59.4% PIVOT at N=700; every "
      "PERSIST-nudging retune overshot to 70–88% PERSIST). The Department Reorganisation scenario "
      "(ADOPT/WAIT) was iterated through 7 versions and accepted at exactly 100/100."),
    N("Calibration history note — C1: Earlier calibration passes produced a stable 57–58% PACKAGE_A "
      "lean under the multi-agent design. The direct single-call method accepted at 51.5% PACKAGE_A, "
      "consistent with sampling variance around a slightly A-favoured mode."),
    N("Calibration history note — C2: An original three-option design (APPROVE / AMEND / REJECT) "
      "was retired after all 8 AMEND-wording variants produced 100% AMEND at N=20. The binary "
      "APPROVE/REJECT prompt was accepted at exactly 100/100."),
    SP(6),
    P("Raw calibration data: <b>experiments/phase0_baseline_calibration/results/raw/evals/</b> — "
      "one JSON file per API call, immutable after writing. Scoring script: "
      "<b>code/phase0_score_complex_direct.py</b> and <b>code/phase0_score_simple.py</b>. "
      "Prompt-version history: <b>experiments/phase0_baseline_calibration/questions/archive/</b>."),
]

# Phases 1–5
story += [
    H("Phase 1 — Pilot run", h2),
    P("Select one simple problem that passed Phase 0 calibration. Sample 20 agents from the joint "
      "distribution under a single configuration. Run the problem. Verify:"),
    B("Responses are not identical — the architecture produces variance"),
    B("Responses are not random — variance is tractable to parameter values"),
    B("Correlation check: do high-TfA agents choose differently from low-TfA?"),
    P("If yes, proceed to Phase 2. If no, the injection mechanism needs work — likely indicates "
      "the system prompt is being treated as flavour rather than as instruction."),

    H("Phase 2 — Simple-problem experiment (full)", h2),
    P("For each surviving simple problem:"),
    B("<b>Sample size:</b> N = 200 agents per configuration"),
    B("<b>Configurations:</b> Run across the defensible subset (8–12 of the 32, including the "
      "Milgram-analogue configuration 00100 and its inverse)"),
    B("<b>Record:</b> decision, reasoning text, full parameter vector"),
    B("<b>Aggregate:</b> decision rate per configuration; logistic regression of decision on "
      "parameter values (within and across configurations); within-configuration variance"),
    P("The reasoning text is valuable qualitative data — spot-check it to verify agents are "
      "reasoning from the parameter profile rather than producing boilerplate."),

    H("Phase 3 — Complex-problem experiment", h2),
    P("For each complex problem:"),
    B("<b>Agent count per run:</b> 5 for C1, 6 for C2, 4 for C3"),
    B("<b>Runs per configuration:</b> 20 (each run uses a fresh parameter draw from the "
      "configuration's joint distribution)"),
    B("<b>Orchestration:</b> Agents of Chaos codebase, adapted for parameter injection"),
    B("<b>Record:</b> full transcript of every round; vote/allocation/information-sharing outcomes; "
      "coalition patterns; round-level state"),
    B("<b>Aggregate:</b> outcome distributions across configurations; transcript qualitative "
      "analysis for flagship differences between configurations"),

    H("Phase 4 — Statistical analysis", h2),
    P("Across simple and complex problems, the analysis structure is the same: configuration is "
      "the primary independent variable; parameter vector is the continuous within-configuration "
      "variance. Tests include:"),
    B("Between-configuration: ANOVA or non-parametric equivalent on decision rates / allocation outcomes"),
    B("Within-configuration: regression of decision on parameter values"),
    B("Interaction: which parameters matter most in which configurations — this is where the "
      "architecture reveals its structure"),
    B("Robustness: re-run across random seeds; re-run with R matrix variants per the "
      "three-regime sensitivity plan"),

    H("Phase 5 — Reporting", h2),
    P("Report configuration-level statistics, not individual-level. Always include Phase 0 "
      "baseline-calibration numbers in the methodology section so readers can verify the 50/50 "
      "constraint was met. Flag cells where effects were smaller than expected — these indicate "
      "either parameters that do less work than theorised, or problems with the injection "
      "mechanism, both of which matter for the framework's credibility."),
]

# ── 7. Summary table ───────────────────────────────────────────────────────────
story += [
    H("7. Summary — The Six Problems at a Glance"),
]
summary_rows = [
    ["ID", "Problem", "Primary Parameters", "Concept Clusters", "Route / Agents"],
    ["S1", "Promotion Decision",       "TfA, RE, MS, PD",       "Justice-Loyalty",              "LPM / N=200 per config"],
    ["S2", "The Quiet Error",          "ID, LL, TfA, RT, MS",   "Authority-Loyalty-Care",       "LPM / N=200 per config"],
    ["S3", "Dept. Reorganisation",     "MoR, RE, MS, PD, RT",   "Care-Justice\n(Camuffo-native)","LPM / N=200 per config"],
    ["C1", "Resource Council",         "TfA, MS, PD, RE, LL",   "Structural\n(group decision)", "AoC / 5 agents × 20 runs"],
    ["C2", "Restructuring Board",      "LL, ID, TfA, MS, Care", "Hierarchical\n(Milgram-analogue)","AoC / 6 agents × 20 runs"],
    ["C3", "Scientific-Approach",      "MoR, RT, MS, AW, ID",   "Epistemic\n(Camuffo-native)",  "AoC / 4 agents × 20 runs"],
]
story.append(results_table(summary_rows, [0.06, 0.20, 0.22, 0.25, 0.27]))

# ── 8. Known Risks ─────────────────────────────────────────────────────────────
story += [
    H("8. Known Risks and Contingencies"),
    B("<b>S3 startup-pivot scenario retired (resolved).</b> The original scenario had a structural "
      "59.4% PIVOT mode that could not be corrected by wording retunes. Replaced by Department "
      "Reorganisation (ADOPT/WAIT), which calibrated to exactly 50/50 at N=200."),
    B("<b>Injection mechanism may produce roleplay rather than encoded reasoning.</b> Pilot-run "
      "diagnostic in Phase 1 catches this. Fix: tool-based injection rather than system-prompt "
      "injection."),
    B("<b>Complex problems may produce variance too large to distinguish configurations.</b> With "
      "only 20 runs per configuration, the signal-to-noise ratio could be thin. Increase to 40 "
      "runs if initial variance is high."),
    B("<b>Parameter-to-decision mapping may be stronger for some parameters than others.</b> "
      "Expected. Report openly; use this to refine the parameter set in Draft 0.6."),
    B("<b>Cross-agent information leakage in complex problems.</b> Orchestrator must enforce "
      "private-evidence boundaries, especially in C3. Audit transcripts for leaks."),
    B("<b>Configurations defined as binary may be too coarse.</b> If within-configuration variance "
      "dominates between-configuration variance, move to continuous configurations in Draft 0.6."),
    SP(20),
    Paragraph(
        "Experimental Problems Specification — April 2026. "
        "Draft 0.2 (updated May 2026), not for citation.",
        ParagraphStyle("footer", parent=base["Normal"],
                       fontSize=8, fontName="Helvetica-Oblique",
                       alignment=TA_CENTER, textColor=colors.HexColor("#888888"))
    ),
]

doc.build(story)
print(f"PDF written to: {OUT}")
