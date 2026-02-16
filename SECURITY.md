# Security Policy

## Reporting Security Issues

If you discover a security vulnerability in IoTShield, please report it to:
- Email: anowarhossain.dev@gmail.com

Please do NOT create public GitHub issues for security vulnerabilities.

## Secure Configuration

### Environment Variables

**NEVER** commit sensitive credentials to Git. Always use environment variables:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual credentials
3. Ensure `.env` is in `.gitignore` (already configured)

### Gmail App Password Security

**IMPORTANT:** Use Gmail App Passwords, not your regular Gmail password.

**Setup:**
1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Add to `.env` file (NEVER commit to Git)
4. Revoke and regenerate if compromised

### API Keys & Credentials

- **Ollama Configuration:** Configure `OLLAMA_HOST` and `OLLAMA_MODEL` in `.env` (local service, no API key needed)
- **Secret Keys:** Generate strong random keys for production
- **MQTT Credentials:** Use authentication in production

## Security Best Practices

### For Development

-  Use `.env` for all sensitive data
-  Keep `.gitignore` updated
-  Regularly rotate credentials
- Use different credentials for dev/prod
-  Never hardcode credentials in source code
-  Never commit `.env` to Git
-  Never share credentials publicly

### For Production

1. **Use HTTPS/TLS:**
   - Enable `USE_TLS=True` in MQTT configuration
   - Use SSL certificates for web server

2. **Database Security:**
   - Use PostgreSQL instead of SQLite
   - Enable authentication
   - Regular backups

3. **MQTT Security:**
   - Enable MQTT authentication
   - Use TLS/SSL for MQTT connections
   - Configure proper ACLs

4. **Django Security:**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS` properly
   - Enable CSRF protection

## Known Security Considerations

### Current Implementation (Development)

- SQLite database (use PostgreSQL in production)
- Local MQTT broker (configure authentication for production)
- Gmail SMTP (consider dedicated email service for production)

### Recommended for Production

- Use environment-specific configuration
- Implement rate limiting
- Add API authentication
- Enable logging and monitoring
- Regular security audits

## Dependency Security

Run security checks regularly:

```bash
# Check for vulnerable dependencies
pip install safety
safety check

# Update dependencies
pip list --outdated
pip install --upgrade package-name
```

## Data Privacy & Local Processing

IoTShield implements privacy-preserving mechanisms:

- Differential privacy noise added to sensor data
- **Local edge processing** with Ollama (no cloud API calls)
- Ollama runs locally on `http://localhost:11434` (optional: configure in `.env`)
- Minimal data collection
- No third-party data sharing
- All AI/ML inference happens on your machine (llama3.2:1b model)

## Incident Response

If credentials are compromised:

1. **Immediately revoke** exposed credentials
2. Generate **new** credentials
3. Update `.env` file with new credentials
4. Remove credentials from Git history (if committed)
5. Review access logs for unauthorized access
6. Monitor for suspicious activity

### Removing Secrets from Git History

If you accidentally committed secrets:

```bash
# WARNING: This rewrites Git history
# Install BFG Repo-Cleaner
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Remove passwords from all commits
bfg --replace-text passwords.txt

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (coordinate with team!)
git push --force
```

**Alternative (for single file):**
```bash
# Remove file from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all

git push --force
```

## Security Updates

- Regularly update dependencies
- Monitor security advisories
- Keep Python, Django, and all packages updated
- Subscribe to security mailing lists

## Contact

For security concerns or questions:
- **Developer:** Anowar Hossain
- **Email:** anowarhossain.dev@gmail.com
- **GitHub:** [@AnowarOHossain](https://github.com/AnowarOHossain)

---

---

## Ollama Security Notes (v2.1+)

- Ollama service runs locally - no internet required for inference
- Model (`llama3.2:1b`) downloaded and runs on your hardware
- API accessible on `http://localhost:11434` (local network only)
- No external API calls for anomaly detection
- All sensor data stays local
- Faster and more private than cloud APIs

**Last Updated:** February 16, 2026
