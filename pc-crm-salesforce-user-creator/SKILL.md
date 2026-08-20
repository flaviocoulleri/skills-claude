---
name: pc-crm-salesforce-user-creator
version: 1.0.0
description: >
  Guides Salesforce admins through bulk user creation from spreadsheets (.xlsx,
  .csv), images/screenshots, or manually dictated lists. Handles the full
  lifecycle: input parsing, org selection, username format, license & profile
  assignment, active/password settings, Permission Set and Permission Set Group
  assignment, validation, and deployment via SF CLI. Use this skill whenever the
  user mentions creating Salesforce users, importing a user list, onboarding
  users in bulk, setting up SF accounts from a spreadsheet, or deploying users
  to a sandbox/production — even if they just say "I have a list of users to
  create" or "need to add users to my org". Works in Spanish and English.
---

<!-- Changelog
1.0.0 (2026-04-25): Primera versión formal bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde `sf-user-creator` → `pc-crm-salesforce-user-creator`. Sin cambios funcionales.
-->

# SF User Creator

Expert Salesforce admin assistant for bulk user creation. Guides the process with best practices, validation, and a structured 5-phase workflow. Speaks the admin's language (Spanish/English).

## Accepted Inputs

1. **Spreadsheet** — .xlsx, .csv, Google Sheets with columns: Nombre, Apellido, Correo (or Name, Last Name, Email).
2. **Image** — Screenshot/photo of a user list.
3. **Manual input** — Users dictated in chat (e.g., "Juan Perez juan@company.com, Maria Lopez maria@company.com").

---

## TOKEN OPTIMIZATION RULES

Follow strictly to reduce token consumption:

### Windows CLI Compatibility (CRITICAL)
On Windows, `sf` CLI lives in `C:\Program Files\sf\bin\sf` — the space in the path breaks direct bash invocations. **ALWAYS use the .bat file pattern** for any `sf` command that contains SOQL or complex arguments:

```bash
# Pattern: write a .bat file, then execute it via cmd, then pipe output to python
cat > /tmp/sf_query.bat << 'EOF'
@echo off
sf data query -q "YOUR SOQL HERE" -o <alias> --json
EOF
cmd //c /tmp/sf_query.bat 2>/dev/null | python -c "
import sys,json
d=json.load(sys.stdin)
# ... parse results
"
```

**Why:** bash→cmd quote escaping mangles SOQL commas and spaces. A .bat file preserves quotes exactly as written.

**Exception:** `sf org list --json` works directly because it has no SOQL argument with commas/spaces. Pipe it through python as usual.

### Minimize CLI output
- **NEVER dump raw JSON** from CLI commands. Always pipe through `python -c` to extract only needed fields.
- Use targeted SOQL instead of full describe calls. Example queries (use .bat pattern above):
  ```sql
  -- List profiles (lightweight)
  SELECT Id, Name FROM Profile WHERE UserType='Standard' ORDER BY Name

  -- List Permission Sets
  SELECT Id, Label FROM PermissionSet WHERE IsOwnedByProfile=false AND IsCustom=true ORDER BY Label

  -- List Permission Set Groups
  SELECT Id, MasterLabel FROM PermissionSetGroup ORDER BY MasterLabel

  -- Check existing usernames
  SELECT Username FROM User WHERE Username IN ('user1@example.com','user2@example.com')

  -- Check available licenses
  SELECT Name, TotalLicenses, UsedLicenses FROM UserLicense WHERE TotalLicenses > 0

  -- Check profile license
  SELECT Id, Name, UserLicense.Name FROM Profile WHERE Name='System Administrator' LIMIT 1
  ```

### Batch admin questions
- **Group related questions in a single message.** Present all decisions for a phase together.
- Combine org selection + username format + license/profile into one question block (Phase 2).
- Combine active/password + PS/PSG assignment into one block (Phase 3).

### Generate scripts inline
- **NEVER use subagents/Agent tool** for user creation. Write scripts directly using the Write tool.
- Create all users in a single Apex anonymous script or CSV for Data Loader.

### Keep responses concise
- Use tables for summaries, not prose.
- Don't repeat information the admin already confirmed.

---

## The 5-Phase Workflow

### PHASE 1: INPUT PARSING (Step 1)

**Step 1 — Parse User List**

Extract and normalize user data from the provided input. Show a summary table:

| # | Nombre | Apellido | Email |
|---|--------|----------|-------|
| 1 | Juan   | Perez    | juan.perez@company.com |
| 2 | Maria  | Lopez    | maria.lopez@company.com |

- Validate all emails have correct format.
- Flag duplicates within the list.
- Flag rows with missing required fields.
- If input is an image, use OCR to extract data and confirm with admin.
- Intro: "Leí tu lista de usuarios. Acá va el resumen — confírmame que los datos estén correctos antes de avanzar."

> **Wait for admin confirmation before proceeding.**

---

### PHASE 2: ENVIRONMENT & CONFIGURATION (Steps 2-5)

Present ALL of these together in ONE message:

**Step 2 — Select Org**

Run `sf org list --json` piped through python to extract only alias, username, and status. This command works directly (no .bat needed — no SOQL):

```bash
sf org list --json 2>/dev/null | python -c "
import sys,json
d=json.load(sys.stdin)
for t in ['nonScratchOrgs','scratchOrgs']:
    for o in d.get('result',{}).get(t,[]):
        a=o.get('alias','—')
        u=o.get('username','—')
        s=o.get('connectedStatus','Unknown')
        if s=='Connected': print(f'{a} | {u} | {s}')
"
```

Only show **Connected** orgs to avoid confusion with expired/domain-not-found entries.

Ask: "En cual de estas orgs queres crear los usuarios?"

- Intro: "Necesito saber en que org vas a crear los usuarios. Aca estan las que tenes conectadas en tu CLI."

**Step 3 — Username Format**

Ask the admin to choose the username format:

| Opcion | Formato | Ejemplo |
|--------|---------|---------|
| A | Solo el correo | juan.perez@company.com |
| B | Correo + sufijo sandbox | juan.perez@company.com.miSandbox |
| C | Correo + sufijo custom | juan.perez@company.com.test1 |

- If B: auto-detect sandbox name from the org alias/username.
- If C: ask admin for the custom suffix.
- Intro: "El username en Salesforce debe ser unico. En sandboxes generalmente se agrega un sufijo. Que formato queres usar?"

**Step 4 — License & Profile**

Query available licenses and profiles from the org using the .bat pattern:

```bash
# Licenses — write .bat, execute, parse
cat > /tmp/sf_licenses.bat << 'BEOF'
@echo off
sf data query -q "SELECT Name, TotalLicenses, UsedLicenses FROM UserLicense WHERE TotalLicenses > 0" -o <alias> --json
BEOF
cmd //c /tmp/sf_licenses.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for r in d.get('result',{}).get('records',[]):
    t,u=r.get('TotalLicenses',0),r.get('UsedLicenses',0)
    if t>0: print(f'{r[\"Name\"]} | Total:{t} | Usadas:{u} | Disponibles:{t-u}')
"

# Profiles — same pattern
cat > /tmp/sf_profiles.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Name FROM Profile WHERE UserType='Standard' ORDER BY Name" -o <alias> --json
BEOF
cmd //c /tmp/sf_profiles.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for r in d.get('result',{}).get('records',[]): print(f'{r[\"Id\"]} | {r[\"Name\"]}')
"
```

Also query the profile's license to confirm compatibility:
```bash
cat > /tmp/sf_prof_lic.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Name, UserLicense.Name FROM Profile WHERE Name='<ProfileName>' LIMIT 1" -o <alias> --json
BEOF
cmd //c /tmp/sf_prof_lic.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
for r in d.get('result',{}).get('records',[]): print(f'Profile: {r[\"Name\"]} | License: {r.get(\"UserLicense\",{}).get(\"Name\",\"?\")}')"
```

Present available licenses and their remaining count. Ask:
- "Que licencia asignar? (Salesforce, Salesforce Platform, etc.)"
- "Que perfil? (System Administrator, Standard User, otro?)"
- Verify there are enough remaining licenses for all users. **BLOCK if insufficient** and tell admin how many are missing.
- Intro: "Aca estan las licencias disponibles en tu org y los perfiles. Dime cual usar para estos usuarios."

**Step 5 — Locale & Defaults**

Ask (with sensible defaults):
- **Locale:** es_AR / en_US / otro? (default: match org default)
- **Time Zone:** America/Argentina/Buenos_Aires / America/New_York / otro?
- **Email Encoding:** UTF-8 (default)
- Intro: "Estos son los valores regionales. Si todos los usuarios son del mismo pais, puedo usar los mismos para todos."

> **Present Steps 2-5 together. One answer from admin.**

---

### PHASE 3: USER SETTINGS & PERMISSIONS (Steps 6-8)

Present together in ONE message:

**Step 6 — Active & Password**

Ask:
- "Los usuarios se crean activos o inactivos?" (default: activos)
- "Generar contrasena y enviar email de bienvenida?" (default: si)
  - If yes: SF sends the reset password email automatically when `generatePassword` is true.
  - If no: admin will need to manually reset passwords later.
- Intro: "Necesito saber si los usuarios arrancan activos y si les envio el mail para que configuren su contrasena."

**Step 7 — Permission Sets**

Query available Permission Sets from the org (excluding profile-owned) using .bat pattern:

```bash
cat > /tmp/sf_ps.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, Label FROM PermissionSet WHERE IsOwnedByProfile=false AND IsCustom=true ORDER BY Label" -o <alias> --json
BEOF
cmd //c /tmp/sf_ps.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
recs=d.get('result',{}).get('records',[])
if not recs: print('(ninguno)')
for i,r in enumerate(recs,1): print(f'{i}. {r[\"Label\"]}')"
```

Present as numbered list. Ask:
- "Hay que asignar algun Permission Set a estos usuarios? Podes elegir uno o varios, o ninguno."
- Allow multi-select by number.
- Intro: "Si necesitas que los usuarios tengan permisos adicionales mas alla del perfil, elígeme los Permission Sets a asignar."

**Step 8 — Permission Set Groups**

Query available PSGs using .bat pattern:

```bash
cat > /tmp/sf_psg.bat << 'BEOF'
@echo off
sf data query -q "SELECT Id, MasterLabel FROM PermissionSetGroup ORDER BY MasterLabel" -o <alias> --json
BEOF
cmd //c /tmp/sf_psg.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
recs=d.get('result',{}).get('records',[])
if not recs: print('(ninguno)')
for i,r in enumerate(recs,1): print(f'{i}. {r[\"MasterLabel\"]}')"
```

Present as numbered list. Ask:
- "Hay que agregarlos a algun Permission Set Group? Elige uno o varios, o ninguno."
- Intro: "Los Permission Set Groups agrupan varios PS en uno solo. Si tu org los usa, podes asignarlos aca."

> **Present Steps 6-8 together. One answer from admin.**

---

### PHASE 4: VALIDATION (Steps 9-11)

**Step 9 — Username Collision Check**

Build the final username list and check for existing users in the org using .bat pattern:

```bash
cat > /tmp/sf_check_users.bat << 'BEOF'
@echo off
sf data query -q "SELECT Username FROM User WHERE Username IN ('user1@co.com.sbx','user2@co.com.sbx')" -o <alias> --json
BEOF
cmd //c /tmp/sf_check_users.bat 2>/dev/null | python -c "
import sys,json; d=json.load(sys.stdin)
recs=d.get('result',{}).get('records',[])
if recs:
    for r in recs: print(f'COLISION: {r[\"Username\"]}')
else:
    print('OK - Todos los usernames disponibles')"
```

- Flag any collisions. Ask admin to resolve (skip user, change username, deactivate existing).
- Intro: "Verifico que ningun username ya exista en la org para evitar errores de deploy."

**Step 10 — License Availability Re-check**

Recount available licenses vs number of users to create. Block if insufficient.

**Step 11 — Final Summary**

Present complete summary table:

| # | Nombre | Apellido | Username | Profile | License | Active | PS | PSG |
|---|--------|----------|----------|---------|---------|--------|----|-----|
| 1 | Juan | Perez | juan.perez@co.com.sbx | Sys Admin | Salesforce | Yes | PS1,PS2 | PSG1 |

- Intro: "Aca va el resumen final de TODO lo que se va a crear. Revisa y confirma para proceder."

> **Wait for explicit admin approval before proceeding to deploy.**

---

### PHASE 5: DEPLOYMENT (Steps 12-14)

**Step 12 — Generate Apex Script**

Create an Anonymous Apex script that:
1. Creates all User records in a single DML operation.
2. Handles `generatePassword` parameter.
3. Assigns Permission Sets via `PermissionSetAssignment`.
4. Assigns Permission Set Groups via `PermissionSetAssignment` (with `PermissionSetGroupId`).

Pattern:

```apex
// User creation
List<User> newUsers = new List<User>();

// Get Profile ID
Id profileId = [SELECT Id FROM Profile WHERE Name = '<ProfileName>' LIMIT 1].Id;

User u1 = new User(
    FirstName = 'Juan',
    LastName = 'Perez',
    Email = 'juan.perez@company.com',
    Username = 'juan.perez@company.com.sbx',
    Alias = 'jperez',
    ProfileId = profileId,
    EmailEncodingKey = 'UTF-8',
    LanguageLocaleKey = 'es',
    LocaleSidKey = 'es_AR',
    TimeZoneSidKey = 'America/Argentina/Buenos_Aires',
    IsActive = true
);
newUsers.add(u1);
// ... more users

Database.SaveResult[] results = Database.insert(newUsers, false);

// Report results
Integer success = 0;
Integer fail = 0;
for (Integer i = 0; i < results.size(); i++) {
    if (results[i].isSuccess()) {
        success++;
        System.debug('OK: ' + newUsers[i].Username);
    } else {
        fail++;
        for (Database.Error e : results[i].getErrors()) {
            System.debug('FAIL: ' + newUsers[i].Username + ' - ' + e.getMessage());
        }
    }
}
System.debug('Total OK: ' + success + ' | Total FAIL: ' + fail);
```

For Permission Set assignment (separate script, runs after users are created):

```apex
// Assign Permission Sets
List<PermissionSetAssignment> psAssignments = new List<PermissionSetAssignment>();

List<User> createdUsers = [SELECT Id, Username FROM User WHERE Username IN ('user1@co.com.sbx','user2@co.com.sbx')];
Map<String, Id> userMap = new Map<String, Id>();
for (User u : createdUsers) userMap.put(u.Username, u.Id);

// PS IDs queried earlier
Id ps1Id = '<PermissionSetId>';

for (Id userId : userMap.values()) {
    psAssignments.add(new PermissionSetAssignment(
        AssigneeId = userId,
        PermissionSetId = ps1Id
    ));
}

Database.SaveResult[] psResults = Database.insert(psAssignments, false);
// ... report results same pattern
```

For Permission Set Group assignment:

```apex
// Same pattern but use PermissionSetGroupId instead of PermissionSetId
psAssignments.add(new PermissionSetAssignment(
    AssigneeId = userId,
    PermissionSetGroupId = '<PSGId>'
));
```

**Step 13 — Execute**

Run the Apex script via CLI using .bat pattern:

```bash
cat > /tmp/sf_run_apex.bat << 'BEOF'
@echo off
sf apex run -f "<absolute-path-to-apex-file>" -o <alias> --json
BEOF
cmd //c /tmp/sf_run_apex.bat 2>/dev/null | python -c "
import sys,json
d=json.load(sys.stdin)
r=d.get('result',{})
if r.get('success'):
    print('EJECUCION EXITOSA')
    logs=r.get('logs','')
    for line in logs.split('\n'):
        if 'USER_DEBUG' in line:
            parts=line.split('USER_DEBUG|')
            print(parts[1] if len(parts)>1 else line)
else:
    print('ERROR:', r.get('compileProblem') or r.get('exceptionMessage') or d.get('message','Unknown'))
"
```

**IMPORTANT:** The apex file path in the .bat MUST be an absolute Windows path (e.g., `C:\Users\...\create-users.apex`), not a Unix path.

- If user creation succeeds, run PS/PSG assignment script next.
- If `generatePassword` was requested, passwords are generated automatically by SF on insert — no extra step needed. Use `System.setPassword()` only if admin wants specific passwords.

**Step 14 — Post-Deploy Report**

Present results table:

| # | Username | Status | Errors |
|---|----------|--------|--------|
| 1 | juan.perez@co.com.sbx | OK | — |
| 2 | maria.lopez@co.com.sbx | FAIL | DUPLICATE_USERNAME |

Then:
- "Usuarios creados exitosamente: X/Y"
- If password emails were sent: "Los usuarios recibiran un email para configurar su contrasena."
- If any failures: explain each error and suggest fix.
- End with: "Proximos pasos manuales: [list any remaining manual actions]"

---

## Alias Generation Rules

The `Alias` field is max 8 characters. Generate as:
1. First letter of FirstName + up to 7 chars of LastName (lowercase).
2. If collision, append incremental number.
3. Example: Juan Perez -> `jperez`, Maria Perez -> `mperez`, Miguel Perez -> `mperez1`.

---

## Important Behavioral Notes

- **Never skip a step.** If it doesn't apply, say so in one line and move on.
- **Always wait for admin confirmation** before deploying (Step 11 approval is mandatory).
- **Speak the admin's language.** Spanish input -> Spanish output.
- **Explain "why" briefly** — one sentence per recommendation, not a paragraph.
- **Never dump raw JSON** from CLI commands — always pipe through python to extract only what's needed.
- **Validate license count BEFORE attempting creation** — creating users without licenses causes confusing errors.
- **Use `Database.insert(users, false)`** for partial success — don't let one bad record block the entire batch.
- **Alias must be unique and max 8 chars** — auto-generate and handle collisions.
- **For sandboxes**, auto-detect the sandbox name from the org info to suggest the username suffix.
- **generatePassword behavior**: When User is inserted with `IsActive=true`, call `System.resetPassword(userId, true)` after insert to trigger the welcome email. The second parameter (`true`) sends the email notification.
