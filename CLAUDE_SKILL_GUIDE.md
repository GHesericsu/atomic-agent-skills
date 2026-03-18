# Claude Skill Specification & Best Practices

This guide is synthesized from the official Anthropic "Complete Guide to Building Skills for Claude" (2025). It defines the technical requirements and optimization strategies for creating high-performance Agent Skills.

---

## 📂 1. Directory Structure
A skill must follow this specific hierarchy to be discoverable by OpenClaw, Claude Code, and other compliant agents:

```text
your-skill-name/          # MUST be kebab-case
├── SKILL.md              # REQUIRED: Main instructions (Case-sensitive)
├── scripts/              # OPTIONAL: Executable code (Python, Bash, etc.)
├── references/           # OPTIONAL: Deep-dive docs, API schemas, guides
└── assets/               # OPTIONAL: Templates, icons, fonts, static files
```

> [!CAUTION]
> **No README.md:** Do not include a `README.md` inside the skill folder. All documentation for the agent belongs in `SKILL.md` or `references/`.

---

## 📝 2. Anatomy of `SKILL.md`

The `SKILL.md` file consists of two parts: YAML Frontmatter and the Markdown Body.

### Part A: Frontmatter (The "Trigger" Layer)
The frontmatter is the only part the agent sees initially. It determines if the skill is relevant to the user's request.

```yaml
---
name: your-skill-name        # Must match folder name (kebab-case)
description: >               # Max 1024 characters. NO XML tags (< >).
  Use this skill when... [What it does + When to use it]. 
  Include specific trigger phrases and file types.
---
```

### Part B: The Body (The "Instruction" Layer)
Use clear, hierarchical Markdown. Focus on **imperative language** and **actionable steps**.

```markdown
# Skill Name

## Core Workflow
1. **Step One**: Use `scripts/process.py` to analyze the input.
2. **Step Two**: If [condition], then [action].
3. **Validation**: Check output against the style guide in `references/brand.md`.

## Gotchas
- The database uses soft deletes (always check `deleted_at IS NULL`).
- Table names are pluralized in the API but singular in the schema.

## Examples
- **Scenario**: User asks for "X".
- **Action**: Run the workflow to produce "Y".
```

---

## 🎯 3. Triggering Rules (Optimization)
To ensure the agent loads your skill at the right time, the `description` field must be optimized for semantic matching:

*   **Imperative Phrasing:** Always start with "Use this skill when..."
*   **User Intent:** Match what the user is trying to *achieve* (e.g., "analyze data"), not how the skill works internally.
*   **Specific Keywords:** Include phrases like "Triggers on 'clip this'", "Activate when user asks to 'onboard customer'", or "Use for .fig files."
*   **Conciseness:** Keep it under 300 characters for the best routing performance.

---

## ⚙️ 4. Instruction Style
*   **Actionable Steps:** Use "Run the script," "Analyze the data," "Validate the schema." Avoid passive language.
*   **Avoid Menus:** Do not ask the agent to "Choose from the following options." Instead, provide clear logic: "If the input is a CSV, do X. If it is a JSON, do Y."
*   **Set Clear Defaults:** Provide a preferred "path of least resistance" so the agent doesn't have to ask clarifying questions for every step.
*   **Validation Loops:** Instruct the agent to validate its own work: `1. Do work → 2. Run validator → 3. Fix → 4. Repeat`.

---

## 🧠 5. Progressive Disclosure
Agents use a three-level system to minimize token usage and manage context:

1.  **Level 1 (Frontmatter):** Loaded in every system prompt. Used only for routing/triggering.
2.  **Level 2 (SKILL.md Body):** Loaded only when the skill is triggered. Contains the primary workflow.
3.  **Level 3 (Linked Files):** The agent only reads files in `references/` or `assets/` when specifically instructed by the `SKILL.md` or when it encounters a trigger defined in the workflow.

---

## ⚠️ 6. Critical Gotchas
*   **Naming:** Skills must be `kebab-case`. No spaces, no underscores, no capital letters.
*   **Reserved Names:** You cannot use "Claude" or "Anthropic" in the skill name.
*   **No XML:** Do not use `<` or `>` in the YAML description field; it interferes with the system prompt structure.
*   **Privacy:** Never include hardcoded credentials or API keys in the skill folder.
