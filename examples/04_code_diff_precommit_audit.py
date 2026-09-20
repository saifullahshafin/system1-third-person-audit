#!/usr/bin/env python3
"""
Example 4: Pre-Commit Code Diff Safety Audit
Demonstrates auditing a git diff before committing code to catch hardcoded secrets
or breaking API changes.
"""

from system1.security import audit_code

VULNERABLE_DIFF = """
--- a/config/database.py
+++ b/config/database.py
@@ -10,3 +10,5 @@
+DATABASE_URL = "postgres://admin:supersecretpassword123@prod-db.internal:5432/main"
+API_KEY = "ts_live_998877665544332211"
"""

def main():
    print("Auditing vulnerable git diff with System One...")
    res = audit_code(VULNERABLE_DIFF, context="Pre-commit git hook")

    print(f"Status:                   {res['status']}")
    print(f"Risk Category:            {res['risk_category']}")
    print(f"Risk Tier Score:          {res['risk_tier_score']:.2f} / 2.0")
    print(f"Blocked:                  {res['is_blocked']}")
    print(f"Requires Human Approval:  {res['requires_human_approval']}")

if __name__ == "__main__":
    main()
