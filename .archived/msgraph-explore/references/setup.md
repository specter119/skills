# Setup

## Environment Variables

Copy `.env.example` to your project directory or the skill directory:

```bash
cp skills/msgraph-explore/.env.example /path/to/project/.env
```

Required variables:

| Variable | Description |
| --- | --- |
| `MICROSOFT_CLIENT_ID` | Azure AD app registration client ID |
| `MICROSOFT_AUTHORITY` | `https://login.microsoftonline.com/<tenant-id>` |
| `MICROSOFT_REFRESH_TOKEN` | Can be left empty on first run; will be written back automatically after login |

## Permissions

Configure all on a single delegated app registration:

- `Sites.Read.All`
- `Notes.Read.All`
- `Files.Read.All`

Scripts request minimum scope per command:

- Search: `Sites.Read.All` + `Files.Read.All`
- OneNote: `Sites.Read.All` + `Notes.Read.All`
- Drive: `Sites.Read.All` + `Files.Read.All`
