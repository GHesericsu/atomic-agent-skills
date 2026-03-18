# Troubleshooting Guide

Common issues when building, testing, and deploying skills, with proven solutions.

---

## Upload & Installation Issues

### Error: "Could not find SKILL.md in uploaded folder"

**Cause:** File is not named exactly `SKILL.md`

**Solutions:**
1. Rename to `SKILL.md` (case-sensitive - not `skill.md` or `SKILL.MD`)
2. Verify with: `ls -la` should show `SKILL.md`
3. Check file is at root of skill folder (not in subdirectory)

```bash
# Correct structure
your-skill/
├── SKILL.md          ✅ At root level
└── scripts/

# Wrong structure
your-skill/
└── docs/
    └── SKILL.md      ❌ In subdirectory
```

---

### Error: "Invalid frontmatter"

**Cause:** YAML formatting issue

**Common mistakes:**

```yaml
# Wrong - missing delimiters
name: my-skill
description: Does things

# Wrong - unclosed quotes
name: my-skill
description: "Does things

# Wrong - inconsistent indentation
name: my-skill
metadata:
author: Me
  version: 1.0

# Correct
---
name: my-skill
description: Does things
metadata:
  author: Me
  version: 1.0
---
```

**Solutions:**
1. Ensure `---` delimiters at start and end
2. Use consistent 2-space indentation
3. Quote strings with special characters
4. Test YAML syntax with online validator
5. Check for tabs (use spaces only)

---

### Error: "Invalid skill name"

**Cause:** Name has spaces, capitals, or invalid characters

**Examples:**

```yaml
# Wrong
name: My Cool Skill      ❌ Capitals and spaces
name: my_cool_skill      ❌ Underscores
name: my.cool.skill      ❌ Periods
name: my cool-skill      ❌ Space

# Correct
name: my-cool-skill      ✅ kebab-case only
```

**Solutions:**
1. Use lowercase letters only
2. Use hyphens for word separation
3. No spaces, underscores, or periods
4. Match folder name exactly

---

### Skill won't appear after upload

**Possible causes:**
1. Skill folder not properly compressed
2. Invalid folder structure
3. Caching issue

**Solutions:**

```bash
# Verify folder structure
cd your-skill-name
ls -la
# Should see SKILL.md at root

# Compress properly (from parent directory)
cd ..
zip -r skill-name.zip skill-name/

# Or use .skill extension
zip -r skill-name.skill skill-name/

# Check archive contents
unzip -l skill-name.zip
# Should show skill-name/SKILL.md at top
```

If structure is correct:
1. Reload Claude.ai/Code
2. Clear browser cache
3. Try re-uploading
4. Check for any console errors

---

## Triggering Issues

### Skill doesn't trigger (under-triggering)

**Symptom:** Skill never loads automatically, requires manual enabling

**Diagnosis:**
Ask Claude: "When would you use the [skill-name] skill?"
Claude will quote the description back, showing how it interprets when to use it.

**Common causes:**

1. **Description too generic**
```yaml
# Bad - too vague
description: Helps with projects

# Good - specific triggers
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".
```

2. **Missing trigger phrases**
```yaml
# Bad - no user-language triggers
description: Implements the Project entity model with hierarchical relationships

# Good - includes what users say
description: Creates project structures in Notion. Use when user says "set up project", "create workspace", "initialize project", or "new Notion project".
```

3. **No file type mentions** (if relevant)
```yaml
# Bad
description: Processes documents

# Good
description: Processes PDF legal documents for contract review. Use when user uploads PDF contracts or asks to "review contract", "extract contract terms", or "analyze legal PDF".
```

**Solutions:**

1. **Add specific trigger phrases** users would actually say
2. **Include synonyms** and paraphrased versions
3. **Mention file types** if skill works with specific formats
4. **Reference common tasks** users want to accomplish
5. **Use action verbs** that describe what users want to do

**Testing approach:**
```
Test queries:
✅ "Help me plan this sprint" (obvious)
✅ "I need to set up tasks for next week" (paraphrased)
✅ "Can you organize my project work?" (indirect)

If skill doesn't trigger on these, revise description.
```

---

### Skill triggers too often (over-triggering)

**Symptom:** Skill loads for unrelated queries, becomes annoying

**Common causes:**

1. **Too broad**
```yaml
# Bad
description: Processes documents

# Better
description: Processes PDF legal documents for contract review
```

2. **Missing scope boundaries**
```yaml
# Bad
description: Helps with data analysis

# Better
description: Advanced statistical analysis for CSV files. Use for regression, clustering, modeling. Do NOT use for simple data exploration (use data-viz skill instead).
```

**Solutions:**

1. **Add negative triggers**
```yaml
description: PayFlow payment processing for e-commerce. Use specifically for online payment workflows, not for general financial queries or accounting tasks.
```

2. **Be more specific about scope**
```yaml
# Before
description: Creates reports

# After
description: Creates quarterly financial reports from accounting system data. Use when user asks for "Q1 report", "quarterly financials", or "earnings report". NOT for ad-hoc data reports.
```

3. **Clarify vs. other skills**
```yaml
description: Advanced data analysis for CSV files. Use for statistical modeling, regression, clustering. For simple data exploration, use data-viz skill instead.
```

4. **Specify domain or context**
```yaml
# Before
description: Manages tasks

# After
description: Manages Linear engineering tasks specifically. Use for sprint planning, bug tracking, and development workflows. NOT for general todo lists or personal tasks.
```

**Testing approach:**
```
Unrelated queries that should NOT trigger:
❌ "What's the weather?"
❌ "Help me write an email"
❌ "Create a simple spreadsheet"

If skill triggers on these, add negative triggers or narrow scope.
```

---

## Execution Issues

### Instructions not followed

**Symptom:** Skill loads but Claude doesn't follow the instructions properly

**Common causes:**

1. **Instructions too verbose**
   - Move detailed docs to `references/`
   - Keep SKILL.md concise
   - Use bullet points and numbered lists

```markdown
# Bad - too much detail in SKILL.md
## Processing Workflow
First, you need to understand that the processing system works by...
[5 paragraphs of explanation]

# Good - concise with references
## Processing Workflow
1. Validate input: `python scripts/validate.py`
2. Process data: See [references/processing.md](references/processing.md)
3. Generate output
```

2. **Critical instructions buried**
   - Put important info at the top
   - Use headers like `## IMPORTANT` or `## CRITICAL`
   - Repeat key points if needed

```markdown
# Good structure
## CRITICAL: Validation Requirements
Before calling create_project, verify:
- Project name is non-empty
- At least one team member assigned
- Start date is not in the past

[Rest of instructions...]
```

3. **Ambiguous language**

```markdown
# Bad
Make sure to validate things properly

# Good
CRITICAL: Run validation before each API call:
\`\`\`bash
python scripts/validate.py --input {file}
\`\`\`

If validation fails, check for:
- Missing required fields (add to CSV)
- Invalid date formats (use YYYY-MM-DD)
- Duplicate entries (remove or merge)
```

4. **Model "laziness" / insufficient encouragement**

Add explicit encouragement:

```markdown
## Performance Notes
- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip validation steps
- Double-check all outputs before finalizing
```

**Pro tip:** This is more effective in user prompts than in SKILL.md

5. **Instructions need to be deterministic**

For critical operations, use scripts instead of text instructions:

```markdown
# Instead of:
"Calculate the checksum and verify it matches"

# Use:
\`\`\`bash
python scripts/verify_checksum.py --file {filename}
\`\`\`
```

**Advanced technique:** Bundle validation scripts for fragile operations. Code is deterministic; language instructions aren't.

---

### MCP Connection Issues

**Symptom:** Skill loads but MCP tool calls fail

**Diagnostic checklist:**

1. **Verify MCP server is connected**
```
Claude.ai: Settings > Extensions > [Your Service]
Should show: "Connected" status
```

2. **Test MCP independently**
Ask Claude directly (without skill):
```
"Use [Service] MCP to fetch my projects"
```
If this fails, issue is MCP configuration, not the skill.

3. **Check authentication**
- API keys valid and not expired
- Proper permissions/scopes granted
- OAuth tokens refreshed
- Credentials stored correctly

4. **Verify tool names**
- Skill references correct MCP tool names
- Tool names are case-sensitive
- Check MCP server documentation
- Confirm available tools: Ask Claude "What tools does [Service] MCP provide?"

**Common authentication errors:**

```
Error: "Authentication failed"
Solutions:
1. Regenerate API key in service dashboard
2. Update key in Claude settings
3. Verify scope/permissions include required operations
4. Check for IP restrictions or rate limits
```

```
Error: "Invalid token"
Solutions:
1. Refresh OAuth token (Settings > Extensions > Reconnect)
2. Check token expiration date
3. Re-authorize application
```

**Rate limiting:**

If seeing intermittent failures:
1. Add delays between API calls
2. Implement exponential backoff
3. Check service's rate limit documentation
4. Consider batching operations

```markdown
# In SKILL.md
## Rate Limiting
This API has limits:
- 100 requests/minute
- 1000 requests/hour

Skill automatically adds delays between calls.
```

---

### API Calls Failing

**Symptom:** MCP connected but specific operations fail

**Debugging approach:**

1. **Check error message**
```
"Permission denied" → Scope/auth issue
"Not found" → Wrong ID/endpoint
"Invalid parameter" → Check data format
"Rate limit exceeded" → Add delays
```

2. **Verify parameters**
```markdown
# In SKILL.md, specify exact format
## Parameters
- project_id: String, format "PRJ-12345"
- date: String, format "YYYY-MM-DD"
- status: Enum ["pending", "active", "complete"]
```

3. **Add validation before API calls**
```markdown
Before calling create_task:
1. Validate: title is non-empty
2. Validate: assigned_to is valid user_id
3. Validate: due_date is future date
4. Only then: Call MCP create_task tool
```

4. **Implement error handling**
```markdown
## Error Handling

If create_project fails:
1. Check if project name already exists
2. Verify user has create permissions
3. Try with simpler name (remove special chars)
4. If still failing, report error to user

If update fails:
1. Confirm item exists
2. Check if locked by another user
3. Verify update permissions
4. Retry once after 2 seconds
```

---

## Performance Issues

### Skill seems slow or responses degraded

**Causes:**

1. **Skill content too large**
   - Move detailed docs to `references/`
   - Keep SKILL.md under 5,000 words
   - Use progressive disclosure

2. **Too many skills enabled simultaneously**
   - Evaluate if you have >20-50 skills enabled
   - Disable unused skills
   - Consider skill "packs" for related capabilities

3. **All content loaded instead of progressive disclosure**

**Optimization strategies:**

```markdown
# Instead of putting everything in SKILL.md:

# SKILL.md (concise overview)
## Advanced Features
For detailed documentation, see:
- [API Reference](references/api.md)
- [Examples](references/examples.md)
- [Troubleshooting](references/troubleshooting.md)

# Only loaded when Claude needs them
```

**File organization:**
```
skill-name/
├── SKILL.md           # <500 lines, core workflow
└── references/
    ├── api.md         # Loaded as needed
    ├── examples.md    # Loaded as needed
    └── advanced.md    # Loaded as needed
```

---

### Large Context Issues

**Symptom:** Performance degradation with complex workflows

**Solutions:**

1. **Split reference files by domain**
```
references/
├── finance.md      # Only loaded for finance queries
├── sales.md        # Only loaded for sales queries
└── product.md      # Only loaded for product queries
```

2. **Add grep patterns for large files**
```markdown
# In SKILL.md
For database schema details, grep `references/schema.md`:
- Table definitions: grep "^### Table:"
- Relationships: grep "^#### Foreign Keys"
```

3. **Use table of contents in long files**
```markdown
# references/api.md

## Contents
1. Authentication
2. Project Management
3. Task Operations
4. User Management

[Full content below...]
```

---

## Testing Issues

### Inconsistent results across test runs

**Causes:**
1. Non-deterministic instructions
2. Missing validation steps
3. Context-dependent behavior
4. Race conditions with async operations

**Solutions:**

1. **Add explicit validation**
```markdown
After each step:
1. Verify operation succeeded
2. Check output matches expected format
3. Confirm all required fields present
```

2. **Use scripts for deterministic operations**
```bash
# Instead of: "Calculate and verify"
# Use:
python scripts/calculate_and_verify.py --input data.csv
```

3. **Add wait conditions**
```markdown
After creating resource:
1. Wait for creation to complete (check status)
2. Verify resource accessible
3. Then proceed to next step
```

---

### Test coverage insufficient

**Minimal test cases needed:**

**Triggering (10-20 queries):**
- 5+ queries that SHOULD trigger (obvious)
- 3+ paraphrased variations (indirect)
- 5+ queries that should NOT trigger (unrelated)

**Functionality:**
- Happy path (everything works)
- Missing inputs (what happens?)
- Invalid inputs (error handling)
- Edge cases (boundaries)
- MCP failures (if applicable)

**Performance:**
- Token usage (compare with/without skill)
- API call efficiency (count calls)
- Time to completion
- User corrections needed

---

## Publishing Issues

### Skill works locally but fails when shared

**Common causes:**

1. **Absolute paths instead of relative**
```markdown
# Bad
See /Users/me/skills/my-skill/references/api.md

# Good
See [references/api.md](references/api.md)
```

2. **Environment-specific dependencies**
```yaml
# In frontmatter
compatibility: "Requires Python 3.9+, requests library, API key in environment"
```

3. **Missing files in package**
```bash
# Verify archive includes everything
unzip -l skill-name.zip
# Should see all scripts, references, assets
```

---

## Getting Help

**When stuck:**

1. **Review this guide** thoroughly
2. **Check example skills** in anthropics/skills repo
3. **Test trigger description** by asking Claude when it would use the skill
4. **Simplify** - Start with minimal working version, then expand
5. **Ask community** - Claude Developers Discord

**Before asking for help, provide:**
- Skill name and description
- Expected vs. actual behavior
- Test queries tried
- Error messages (full text)
- What you've tried already

**Debug checklist:**
```bash
# 1. Verify file structure
ls -la skill-name/

# 2. Check YAML syntax
head -n 20 skill-name/SKILL.md

# 3. Test trigger description
# Ask Claude: "When would you use the [skill-name] skill?"

# 4. Verify MCP (if applicable)
# Ask Claude: "What tools does [Service] MCP provide?"

# 5. Check for secrets
grep -r "api_key\|sk-\|secret" skill-name/
```

---

## Quick Reference: Common Fixes

| Problem | Quick Fix |
|---------|-----------|
| Won't upload | Check SKILL.md spelling (case-sensitive) |
| Invalid frontmatter | Add `---` delimiters, fix indentation |
| Won't trigger | Add specific trigger phrases to description |
| Triggers too often | Add negative triggers, narrow scope |
| Instructions ignored | Move details to references/, be more specific |
| MCP fails | Test MCP independently first |
| Slow performance | Split into references/, reduce SKILL.md size |
| Inconsistent results | Add validation steps, use scripts |

---

**Remember:** Most issues are fixable by making the description more specific or instructions more concise. Start there.
