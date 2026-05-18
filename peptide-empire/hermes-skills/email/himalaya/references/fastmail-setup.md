# Fastmail Email Setup for Hermes + Himalaya

## Fastmail Account Setup

1. Sign up at fastmail.com (30-day free trial, $5/mo Basic)
2. Add your custom domain in Settings → Domains
3. **Create App Password:** Settings → Privacy & Security → App Passwords → New App Password
   - Name: "Hermes Agent"
   - Access: Mail (IMAP/SMTP)
   - Copy the generated password — shown only once

## DNS Records (Add at Domain Registrar — e.g., Porkbun, Namecheap)

### MX Records
| Type | Host | Answer | Priority |
|------|------|--------|----------|
| MX | @ | in1-smtp.messagingengine.com | 10 |
| MX | @ | in2-smtp.messagingengine.com | 20 |

### SPF + DKIM + DMARC
| Type | Host | Answer |
|------|------|--------|
| TXT | @ | v=spf1 include:spf.messagingengine.com ?all |
| CNAME | fm1._domainkey | fm1.YOURDOMAIN.COM.dkim.fmhosted.com |
| CNAME | fm2._domainkey | fm2.YOURDOMAIN.COM.dkim.fmhosted.com |
| CNAME | fm3._domainkey | fm3.YOURDOMAIN.COM.dkim.fmhosted.com |
| TXT | _dmarc | v=DMARC1; p=none; |

## Himalaya Configuration

Create `~/.config/himalaya/config.toml`:

```toml
[accounts.primary]
email = "you@yourdomain.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.fastmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@yourdomain.com"
backend.auth.type = "password"
backend.auth.cmd = "echo 'YOUR_APP_PASSWORD'"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.fastmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@yourdomain.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "echo 'YOUR_APP_PASSWORD'"
```

Secure it: `chmod 600 ~/.config/himalaya/config.toml`

## Test the Connection

```bash
# List folders (verifies IMAP)
himalaya folder list

# Send test email
cat << 'EOF' | himalaya template send
From: Your Name <you@yourdomain.com>
To: you@yourdomain.com
Subject: Test from Hermes

Email system is live. Sent via himalaya + Fastmail.
EOF
```

## Sending from Hermes Skills

When a skill needs to send email, use this pattern:

```bash
cat << 'EOF' | himalaya template send
From: Your Name <you@yourdomain.com>
To: recipient@example.com
Subject: Subject Line

Email body here. Include disclaimer if applicable.

--
Your Name
you@yourdomain.com
EOF
```

Do NOT use `himalaya message write` without piped input — it opens $EDITOR interactively and will hang in automated contexts.

## Common Fastmail Settings

| Setting | Value |
|---------|-------|
| IMAP Server | imap.fastmail.com |
| IMAP Port | 993 |
| IMAP Encryption | SSL/TLS |
| SMTP Server | smtp.fastmail.com |
| SMTP Port | 587 |
| SMTP Encryption | STARTTLS |
| Username | Full email address |
| Password | App-specific password (NOT account password) |
