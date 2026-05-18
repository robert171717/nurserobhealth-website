# Zapier MCP Server Setup for Hermes

Step-by-step guide for connecting Zapier's 8,000+ app MCP server to Hermes Agent.

## Dashboard Setup (User Side)

1. **Go to https://mcp.zapier.com** in Chrome/Firefox (NOT Safari — mobile Safari blocks the JavaScript modal)
2. Sign in with Google
3. Click **"+ New MCP Server"**
4. Under "Step 1: Choose client" → click **"Other"** (Hermes isn't listed in the popular AI agents)
5. Go to the **"Connect"** tab (NOT "Apps" — that's for later)
6. Click **"Generate Token"** — copy the MCP Server URL and token

## Hermes Config (Agent Side)

Zapier uses HTTP transport with the token embedded as a query parameter. Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  zapier:
    url: "https://mcp.zapier.com/api/v1/connect?token=<TOKEN>"
    timeout: 180
    connect_timeout: 60
```

The URL IS the full connection string — token goes in the query param, not in headers.

## Tool Selection (Dashboard → Apps Tab)

After config is written, go to **"Apps"** → **"Add Tools"**. Only add what the automation actually needs:

### Discord (for lead alerts)
- Send Channel Message — post to a channel
- Send Direct Message — DM the user
- Find Channel — discover channel IDs
- Find User — look up users by username

**DO NOT grant:** Administrator, Manage Server, Kick/Ban, Manage Roles, Manage Channels, or any other admin permissions. Zapier has zero reason to have root access.

**OAuth scope:** Check ONLY: View Channels, Send Messages, Embed Links, Read Message History.

### Google Sheets (for lead logging / data tracking)
- Create Spreadsheet Row — append new rows
- Find Worksheet — locate the sheet by name

**OAuth scope trap:** Auto-provisioning (the `auto_provision_mcp` tool) gives Google Sheets a RESTRICTED scope set. This is sufficient for reading/writing rows in spreadsheets the user already owns, BUT often fails with:
- `create_spreadsheet` → "Insufficient Permission" (needs Drive.create scope)
- `find_worksheet` / `add_row` on newly-created sheets → "Insufficient authentication scopes" (sometimes needs broader Drive/file scopes)
- `get_spreadsheet_by_id` on sheets not yet opened → may not detect headers

**Workaround:** Create the spreadsheet manually (sheets.new) in the browser, set up headers, then use Zapier only for row operations. If even row operations fail (common with auto-provisioned scopes), share the sheet with a service account and use the Google Sheets REST API directly — bypass Zapier entirely for Sheets. The direct API via service account + `googleapis` Python library is more reliable than Zapier's restricted OAuth scopes.

### Gmail (for welcome emails)
- Send Email — auto-welcome new leads

**OAuth scope:** Check ONLY "Manage drafts and send emails." Do NOT grant "Read, compose, and send emails" (inbox read access) or "delete contacts."

### Cal.com — SKIP
No tool needed. The booking link is static — just include `cal.com/nurserob/peptide-consult` in email body text.

## Pitfalls

- **Mobile Safari broken:** The "New MCP Server" button does nothing on iOS Safari. Use desktop Chrome/Firefox.
- **"Other" is correct:** Hermes isn't in the dropdown. "Other" speaks standard MCP protocol — it works.
- **Token in URL, not header:** Unlike typical HTTP MCP servers that use `headers.Authorization`, Zapier's token IS the URL query parameter.
- **OAuth over-granting:** Google's consent screen lists ALL possible scopes. Only check the minimum required. "Zapier already has some access" means basic auth is done — hit Continue without adding extras.
- **Tools can be added later:** You don't need all tools at once. Add more anytime via the dashboard without changing the Hermes config.
