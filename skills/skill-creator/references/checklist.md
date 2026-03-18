# Pre-Flight Checklist

Use this checklist to validate your skill before and after upload. Run through each section to ensure your skill meets all requirements.

## Before You Start

**Planning & Requirements:**
- [ ] Identified 2-3 concrete use cases with examples
- [ ] Defined success criteria (quantitative & qualitative)
- [ ] Tools identified (built-in Claude capabilities or MCP servers)
- [ ] Reviewed Anthropic's official guide and example skills
- [ ] Planned folder structure (SKILL.md + any bundled resources)
- [ ] Determined which workflow pattern(s) to use

**Environment Check:**
- [ ] Have access to any required MCP servers (if applicable)
- [ ] API keys/credentials configured (if needed)
- [ ] Test environment available for validation

---

## During Development

### Folder & File Structure

**Naming:**
- [ ] Skill folder named in `kebab-case` (e.g., `notion-setup`)
- [ ] No spaces in folder name
- [ ] No capitals in folder name
- [ ] No underscores in folder name
- [ ] Folder name matches skill name in frontmatter

**Required Files:**
- [ ] `SKILL.md` file exists (exact spelling, case-sensitive)
- [ ] No `README.md` inside the skill folder
- [ ] No extraneous documentation files (INSTALLATION_GUIDE.md, etc.)

**Optional Resources (only if needed):**
- [ ] `scripts/` directory for executable code
- [ ] `references/` directory for documentation
- [ ] `assets/` directory for templates/files used in output
- [ ] All bundled resources are actually referenced in SKILL.md

### YAML Frontmatter

**Format:**
- [ ] Starts with `---` delimiter
- [ ] Ends with `---` delimiter
- [ ] Valid YAML syntax (no syntax errors)
- [ ] Proper indentation (2 spaces)

**Required Fields:**
- [ ] `name` field exists
- [ ] `name` is in kebab-case (no spaces, no capitals)
- [ ] `name` matches folder name exactly
- [ ] `description` field exists
- [ ] `description` includes WHAT the skill does
- [ ] `description` includes WHEN to use it (trigger phrases)
- [ ] `description` is under 1024 characters
- [ ] `description` includes terms users would actually say

**Optional Fields (if used):**
- [ ] `license` field is valid (e.g., MIT, Apache-2.0)
- [ ] `compatibility` field describes requirements clearly
- [ ] `metadata` fields are helpful and accurate

**Security:**
- [ ] No XML angle brackets (`<` or `>`) anywhere in frontmatter
- [ ] Skill name doesn't include "claude" or "anthropic" (reserved)
- [ ] No sensitive data (API keys, passwords, secrets)

### Description Quality Check

**Completeness:**
- [ ] Describes the core value proposition
- [ ] Lists specific capabilities
- [ ] Includes trigger phrases users would say
- [ ] Mentions relevant file types (if applicable)
- [ ] Clear about what makes this skill special

**Specificity:**
- [ ] Not too generic ("Helps with projects" ❌)
- [ ] Not too technical without user context
- [ ] Includes concrete examples of when to use
- [ ] Clear boundaries (what it does NOT do)

**Triggering:**
- [ ] Contains keywords users would actually type/say
- [ ] Covers paraphrased variations
- [ ] Specific enough to avoid over-triggering
- [ ] Includes negative triggers if needed ("Do NOT use for...")

### Instructions in SKILL.md Body

**Structure:**
- [ ] Logical organization (Overview → Workflow → Examples → Troubleshooting)
- [ ] Clear headings and sections
- [ ] Under 500 lines (longer content moved to references/)

**Clarity:**
- [ ] Instructions are specific and actionable
- [ ] Steps are numbered or clearly ordered
- [ ] Expected outputs described
- [ ] Error handling included
- [ ] No vague language ("make sure things work" ❌)

**Resources:**
- [ ] Scripts clearly referenced with usage examples
- [ ] Reference files linked with description of when to read them
- [ ] Assets referenced with explanation of purpose
- [ ] No duplication between SKILL.md and reference files

**Best Practices:**
- [ ] Uses progressive disclosure (details in references/)
- [ ] Includes concrete examples
- [ ] Error messages and solutions provided
- [ ] Validation steps between major actions

### Bundled Resources (if applicable)

**Scripts (`scripts/`):**
- [ ] Scripts are executable
- [ ] Scripts have clear names indicating purpose
- [ ] Scripts include usage comments/docstrings
- [ ] Scripts are tested and working
- [ ] Scripts handle errors gracefully

**References (`references/`):**
- [ ] Files contain information not in SKILL.md
- [ ] No duplication with SKILL.md content
- [ ] Large files (>10k words) have grep patterns in SKILL.md
- [ ] Files over 100 lines have table of contents
- [ ] Clear when to load each reference file

**Assets (`assets/`):**
- [ ] Files are used in skill output (not documentation)
- [ ] Templates are clean and well-structured
- [ ] No sensitive data in templates
- [ ] Assets are actually needed (not "nice to have")

---

## Before Upload

### Testing - Triggering

**Should Trigger On:**
- [ ] Obvious direct requests (test 3+ examples)
- [ ] Paraphrased variations (test 3+ examples)
- [ ] Related but indirect requests (test 2+ examples)

**Should NOT Trigger On:**
- [ ] Completely unrelated topics (test 5+ examples)
- [ ] Topics handled by other skills
- [ ] General queries that don't need this skill

**Triggering Analysis:**
- [ ] No under-triggering (skill loads when needed)
- [ ] No over-triggering (skill doesn't load when irrelevant)
- [ ] Description accurately reflects when skill is useful

### Testing - Functionality

**Core Workflow:**
- [ ] Skill completes primary use case successfully
- [ ] Instructions are followed correctly
- [ ] Output quality meets standards
- [ ] All bundled resources work as expected

**Error Handling:**
- [ ] Gracefully handles missing inputs
- [ ] Provides helpful error messages
- [ ] Handles API failures (if using MCP)
- [ ] Recovers from common issues

**Edge Cases:**
- [ ] Tested with minimal inputs
- [ ] Tested with maximum inputs
- [ ] Tested with invalid inputs
- [ ] Tested with unexpected user requests

**MCP Integration (if applicable):**
- [ ] MCP server is connected
- [ ] Tool calls succeed
- [ ] Authentication works
- [ ] API rate limits respected
- [ ] Error handling for MCP failures

### Testing - Performance

**Efficiency:**
- [ ] Token usage is reasonable (not excessive)
- [ ] Completes workflow in expected number of steps
- [ ] No unnecessary API calls
- [ ] Progressive disclosure working (only loads what's needed)

**Comparison (with vs. without skill):**
- [ ] Fewer user corrections needed
- [ ] More consistent results
- [ ] Faster completion time
- [ ] Better output quality

### Quality Assurance

**User Experience:**
- [ ] Instructions are clear and easy to follow
- [ ] Examples are helpful and realistic
- [ ] Error messages guide users to solutions
- [ ] Skill feels polished and professional

**Documentation:**
- [ ] All features are documented
- [ ] Examples cover common scenarios
- [ ] Troubleshooting section is helpful
- [ ] No outdated information

**Metadata:**
- [ ] Author information included (if applicable)
- [ ] Version number set
- [ ] License specified (if open source)
- [ ] MCP server name included (if applicable)

### Final Checks

**Security & Privacy:**
- [ ] No API keys or secrets in skill files
- [ ] No personal/sensitive data
- [ ] No malicious code
- [ ] Follows security best practices

**Packaging:**
- [ ] All necessary files included
- [ ] No unnecessary files (build artifacts, .DS_Store, etc.)
- [ ] Proper directory structure maintained
- [ ] Ready to compress as .zip or .skill file

**Publishing Readiness (if sharing):**
- [ ] Skill is thoroughly tested
- [ ] Documentation is complete
- [ ] License is appropriate
- [ ] No breaking bugs
- [ ] Ready for community use

---

## After Upload

### Initial Testing

**In Production Environment:**
- [ ] Upload successful
- [ ] Skill appears in skill list
- [ ] Can enable/disable skill
- [ ] Triggers correctly in real conversations

**Real Usage:**
- [ ] Test with realistic user queries
- [ ] Verify behavior matches expectations
- [ ] Check for any unexpected issues
- [ ] Validate performance in production

### Monitoring & Iteration

**Usage Patterns:**
- [ ] Monitor when skill triggers
- [ ] Check for under-triggering issues
- [ ] Check for over-triggering issues
- [ ] Collect user feedback

**Quality:**
- [ ] Monitor output quality
- [ ] Track error rates
- [ ] Identify improvement opportunities
- [ ] Document issues for next version

**Iteration Planning:**
- [ ] Create list of improvements
- [ ] Prioritize based on impact
- [ ] Plan next version
- [ ] Update version number in metadata

### Documentation Updates

**If Issues Found:**
- [ ] Update troubleshooting section
- [ ] Add new examples
- [ ] Improve instructions
- [ ] Update description if triggering issues

**If Features Added:**
- [ ] Document new capabilities
- [ ] Add to description (if affects triggering)
- [ ] Update examples
- [ ] Increment version number

---

## Quick Validation Commands

Run these checks before finalizing:

```bash
# Check file structure
ls -la your-skill-name/
# Should see: SKILL.md (and optional scripts/, references/, assets/)

# Validate YAML frontmatter
head -n 10 your-skill-name/SKILL.md
# Should see: --- at top, valid YAML, --- closing

# Check for README.md (should NOT exist inside skill)
find your-skill-name -name "README.md"
# Should return: nothing

# Test scripts (if any)
python scripts/test_script.py --help
# Should run without errors

# Check for secrets/API keys
grep -r "sk-" your-skill-name/
grep -r "api_key" your-skill-name/
# Should return: nothing (or only references to env vars)
```

---

## Common Mistakes to Avoid

- ❌ Forgetting the `---` YAML delimiters
- ❌ Using spaces or capitals in skill name
- ❌ Description too vague ("Helps with projects")
- ❌ Missing trigger phrases in description
- ❌ Including README.md inside skill folder
- ❌ Putting everything in SKILL.md (not using progressive disclosure)
- ❌ Not testing triggering thoroughly
- ❌ Hardcoding values instead of using parameters
- ❌ No error handling
- ❌ Not testing with edge cases
- ❌ Including sensitive data in skill files

---

## Success Indicators

Your skill is ready when:

✅ Triggers automatically on relevant queries  
✅ Doesn't trigger on irrelevant queries  
✅ Completes workflows without user correction  
✅ Provides consistent, high-quality results  
✅ Handles errors gracefully  
✅ Uses context window efficiently  
✅ Works well alongside other skills  
✅ Documentation is clear and helpful  
✅ Passes all checklist items  
✅ You would confidently recommend it to others

---

**Final step:** Run through this entire checklist one more time before publishing. It's worth the extra 10 minutes to ensure quality.
