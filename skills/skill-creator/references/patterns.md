# Five Proven Workflow Patterns

These patterns emerged from real skills created by early adopters and Anthropic teams. They represent common approaches that work well, not prescriptive templates.

## Choosing Your Approach

**Problem-first:** "I need to set up a project workspace" → Your skill orchestrates the right MCP calls in sequence. Users describe outcomes; skill handles tools.

**Tool-first:** "I have Notion MCP connected" → Your skill teaches Claude optimal workflows and best practices. Users have access; skill provides expertise.

Most skills lean one direction. This helps you choose the right pattern below.

---

## Pattern 1: Sequential Workflow Orchestration

**Use when:** Users need multi-step processes in a specific order.

**Example:** Customer onboarding

### Structure

```markdown
## Workflow: Onboard New Customer

### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company
Verify: account_id returned

### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification
Store: payment_method_id

### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)
Verify: subscription active

### Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
Variables: customer_name, login_url
```

### Key Techniques
- **Explicit step ordering** - Number steps clearly
- **Dependencies between steps** - Reference outputs from previous steps
- **Validation at each stage** - Verify success before proceeding
- **Rollback instructions** - What to do if a step fails

### When to Use
- Payment processing workflows
- Multi-service setup procedures
- Onboarding flows
- Data migration tasks

---

## Pattern 2: Multi-MCP Coordination

**Use when:** Workflows span multiple services that need to work together.

**Example:** Design-to-development handoff

### Structure

```markdown
## Multi-Service Handoff Workflow

### Phase 1: Design Export (Figma MCP)
1. Export design assets from Figma
2. Generate design specifications
3. Create asset manifest
Output: asset_list.json

### Phase 2: Asset Storage (Drive MCP)
1. Create project folder in Drive
2. Upload all assets from Phase 1
3. Generate shareable links
Output: asset_links.json

### Phase 3: Task Creation (Linear MCP)
1. Create development tasks
2. Attach asset links to each task
3. Assign to engineering team
Output: task_ids

### Phase 4: Notification (Slack MCP)
1. Post handoff summary to #engineering
2. Include asset links and task references
3. Tag relevant team members
```

### Key Techniques
- **Clear phase separation** - Each MCP gets its own section
- **Data passing between MCPs** - Explicit outputs and inputs
- **Validation before next phase** - Confirm data integrity
- **Centralized error handling** - Single place to catch cross-service issues

### When to Use
- Cross-platform workflows
- Complex data pipelines
- Team collaboration processes
- Multi-tool automation

---

## Pattern 3: Iterative Refinement

**Use when:** Output quality improves with iteration and validation.

**Example:** Report generation

### Structure

```markdown
## Iterative Report Creation

### Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file

### Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues:
   - Missing sections
   - Inconsistent formatting
   - Data validation errors
3. Generate quality score (0-100)

### Refinement Loop
WHILE quality_score < 90:
  1. Address highest-priority issue
  2. Regenerate affected sections
  3. Re-validate
  4. Update quality score
  
MAX_ITERATIONS: 3

### Finalization
1. Apply final formatting
2. Generate executive summary
3. Save final version
4. Create change log
```

### Key Techniques
- **Explicit quality criteria** - Define what "good" looks like
- **Iterative improvement** - Fix issues one at a time
- **Validation scripts** - Deterministic quality checks
- **Know when to stop** - Max iterations or quality threshold
- **Change tracking** - Document what improved

### When to Use
- Document generation
- Code generation and refinement
- Data analysis reports
- Any output requiring high quality standards

---

## Pattern 4: Context-Aware Tool Selection

**Use when:** Same outcome, but different tools depending on context.

**Example:** Smart file storage

### Structure

```markdown
## Smart File Storage

### Decision Tree

1. Check file type and size
2. Determine best storage location:

   IF file_size > 10MB:
     → Use cloud storage MCP
   
   ELSE IF file_type in ['doc', 'docx', 'slides']:
     → Use Notion/Docs MCP
   
   ELSE IF file_type in ['py', 'js', 'md']:
     → Use GitHub MCP
   
   ELSE IF temporary == true:
     → Use local storage
   
   DEFAULT:
     → Ask user for preference

### Execute Storage

Based on decision:
- Call appropriate MCP tool
- Apply service-specific metadata
- Set appropriate permissions
- Generate access link

### Provide Context to User

Explain:
- Why that storage was chosen
- How to access the file
- Any relevant limitations
```

### Key Techniques
- **Clear decision criteria** - Explicit if/else logic
- **Fallback options** - What happens when criteria don't match
- **Transparency about choices** - Tell user why you chose X
- **Graceful degradation** - Handle missing tools

### When to Use
- Multi-tool environments
- Context-dependent workflows
- Optimization decisions
- Resource allocation

---

## Pattern 5: Domain-Specific Intelligence

**Use when:** Your skill adds specialized knowledge beyond simple tool access.

**Example:** Financial compliance checking

### Structure

```markdown
## Payment Processing with Compliance

### Before Processing (Compliance Check)

1. Fetch transaction details via MCP

2. Apply compliance rules:
   
   **Sanctions Check:**
   - Query sanctions lists
   - Verify customer/country not blocked
   - Document check results
   
   **Jurisdiction Verification:**
   - Check if transaction allowed in region
   - Verify licensing requirements
   - Confirm regulatory compliance
   
   **Risk Assessment:**
   - Calculate transaction risk score
   - Apply business rules
   - Flag if score > threshold

3. Generate compliance decision:
   - APPROVED: Proceed to processing
   - REVIEW: Flag for manual review
   - BLOCKED: Reject with reason

### Processing (If Approved)

IF compliance == APPROVED:
  1. Call payment processing MCP tool
  2. Apply fraud detection rules
  3. Process transaction
  4. Generate receipt
  
ELSE IF compliance == REVIEW:
  1. Create compliance case
  2. Assign to review team
  3. Notify relevant parties
  
ELSE:
  1. Reject transaction
  2. Log rejection reason
  3. Notify customer

### Audit Trail

For ALL transactions:
- Log all compliance checks performed
- Record all decisions and reasoning
- Generate audit report
- Store for regulatory retention period
```

### Key Techniques
- **Domain expertise embedded** - Compliance rules in the skill
- **Compliance before action** - Never skip validation
- **Comprehensive documentation** - Every decision logged
- **Clear governance** - Audit trail for regulations
- **Risk-based routing** - Different paths based on risk level

### When to Use
- Regulated industries (finance, healthcare)
- Legal workflows
- Quality control processes
- Any domain requiring specialized knowledge

---

## Combining Patterns

Real skills often combine multiple patterns:

**Example: Enterprise project setup**
- Pattern 1 (Sequential) for overall workflow
- Pattern 2 (Multi-MCP) for cross-service operations
- Pattern 4 (Context-aware) for tool selection
- Pattern 5 (Domain-specific) for company policies

**Example: AI-assisted code review**
- Pattern 3 (Iterative) for code quality improvement
- Pattern 5 (Domain-specific) for security/style rules
- Pattern 1 (Sequential) for review workflow

## Choosing the Right Pattern

Ask yourself:

1. **Is order critical?** → Pattern 1 (Sequential)
2. **Do I need multiple services?** → Pattern 2 (Multi-MCP)
3. **Does quality need iteration?** → Pattern 3 (Iterative)
4. **Do conditions affect tool choice?** → Pattern 4 (Context-aware)
5. **Do I need specialized knowledge?** → Pattern 5 (Domain-specific)

Most skills use 2-3 patterns combined. Start with the primary pattern and layer others as needed.

## Anti-Patterns to Avoid

❌ **Everything in SKILL.md** - Use progressive disclosure
❌ **Vague instructions** - Be specific and actionable
❌ **No error handling** - Always plan for failure cases
❌ **Assuming perfect inputs** - Validate and sanitize
❌ **Ignoring context window** - Keep it concise
❌ **No validation between steps** - Check before proceeding
❌ **Hardcoded values** - Use parameters and configuration
❌ **No rollback strategy** - Plan how to undo failed operations
