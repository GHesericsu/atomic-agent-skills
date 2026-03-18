---
name: skill-creator
description: Use this skill when creating, editing, improving, auditing, or packaging AgentSkills for OpenClaw. Trigger on phrases like "create a skill", "build a skill", "audit our skills", "improve this skill", "publish to clawhub", or "skill structure". It provides expert guidance on optimizing descriptions for triggering, following the Agent Skills spec for SKILL.md files.
---

# Skill Creator

Expert guidance for creating production-ready Agent Skills (OpenClaw / Claude Code).

## Quick Start

1. **Define Intent** - Identify the specific user goals this skill solves.
2. **Design Trigger Queries** - Create 10 "should trigger" and 10 "should not trigger" queries to test.
3. **Initialize** - Run `scripts/init_skill.py <name>`.
4. **Edit SKILL.md** - Focus on the frontmatter `description` first (Must include WHAT + WHEN).
5. **Optimize Triggering** - Follow the [Description Optimization](#the-description-field-critical) guide.
6. **Package & Publish** - Use `scripts/package_skill.py` then `clawhub publish`.

## Core Principles

### Progressive Disclosure

To keep the context window efficient, skills load in three levels:
1. **Frontmatter** (always loaded) - Name + description only (must be concise).
2. **SKILL.md body** (only when triggered) - Core instructions (keep under 500 lines).
3. **Bundled resources** (read as needed) - Scripts, references, and assets.

### The Description Field (Critical)

This is the only field the agent uses to decide whether to load the skill.

**Rules for a Great Description:**
- **Imperative Phrasing:** Always start with "Use this skill when..."
- **User Intent:** Match what the user is trying to achieve (e.g., "analyze data"), not how the skill works.
- **Specific Keywords:** Explicitly list trigger phrases and domain-specific terms.
- **Conciseness:** Must be under **1024 characters**. Keep it under 300 for best results.

**Good Example:**
```yaml
description: >
  Use this skill when the user wants to manage Linear project workflows, including sprint planning
  and task creation. Trigger on keywords like "sprint", "Linear tasks", "new ticket", or "project status".
```

**Bad Example:**
```yaml
description: This skill helps with project management in Linear.
```

## Skill Creation Workflow

### Step 1: Market Research (Search first)
Before building, check if a high-quality skill already exists.
- Use `skillme search "<query>"` to check ClawHub and skills.sh.
- If a good one exists on skills.sh, use `skillme add <url>` to convert and install it.

### Step 2: Initialize & Structure
```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```
- Folder name must be **kebab-case** (e.g., `my-cool-skill`).
- Exactly **SKILL.md** (case-sensitive).
- No README.md inside (SKILL.md is the single source of truth).

### Step 3: Write for the Agent
Write instructions for another AI agent (Codex/Sonnet). 
- Use imperative, actionable steps.
- Put the most critical instructions at the top.
- Reference scripts or files in the `scripts/` or `references/` folders.

### Step 4: Testing & Trigger Eval
Create an eval set of 20 queries:
- **10 Positives:** Varied phrasing, casual vs. formal, context-heavy.
- **10 Near-Misses:** Queries that share keywords but require different skills (e.g., "Excel help" vs. "CSV skill").

### Step 5: Package & Publish
```bash
# Validate and package to .skill zip
scripts/package_skill.py <path/to/skill>

# Publish to the global registry
clawhub publish <path/to/skill>
```

## When to Ask for Help
If the skill logic is too complex for a single markdown file, delegate specific sub-tasks to a Python script in the `scripts/` folder. This keeps the SKILL.md "atomic" and robust.

## Troubleshooting Triggering
- **Skill won't trigger:** Add more user-intent phrases to the description.
- **Triggers too often:** Add negative triggers ("Do NOT use for...") to the description.
- **Instructions ignored:** Shorten the body. Move details into `references/`.
