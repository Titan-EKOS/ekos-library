# Mock agency review prompt (internal use only; output never pasted into a deliverable)

Give the same prompt to two independent reviewer instances on two different AI platforms (set A, set B).

---
You are reviewing the attached draft drainage document before it is submitted. Review it four times, once in each
role, using only the document and the manuals listed.

Roles:
1. Town/city development engineering reviewer (prefix TWN)
2. County flood control district reviewer (prefix FCD)
3. Landowner-agency reviewer, e.g. state land department (prefix LND)
4. Skeptical public reader (prefix PUB) - technical gaps only

Governing manuals: <list with editions>

For every comment give:
- ID: <set letter>-<role prefix>-<nn>, e.g. A-FCD-07 (unique within your set)
- Location: section, page, and table or figure number
- What is missing or wrong
- Expected revision

Do not rewrite the document. Do not comment on punctuation. Flag every flow without a stated return period,
duration and source; every result without a cited model output; every exhibit without scale, legend or storm title.
---

Merge rule: collapse duplicates, keep the stricter wording, record which set raised each item, rank items raised by
both sets first. Discard political framing; keep the technical gap.
