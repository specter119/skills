# Thorough Digest Guidelines

## Parallelization Table

| Total Items | Groups | Items/Group |
|-------------|--------|-------------|
| 1-10 | 1-2 | 5-10 |
| 11-30 | 3-5 | 6-10 |
| 31-50 | 5-8 | 6-10 |
| 51-100 | 8-15 | 5-10 |
| 100+ | 15-20 | 5-10 |

---

## Error Handling

| Error | Action |
|-------|--------|
| Sub-agent skips items | Re-run with smaller group |
| File read fails | Note in gaps, continue |
| Sub-agent timeout | Use partial results |
| Output format wrong | Re-prompt with explicit format |

---

## Best Practices

1. **Small groups**: 5-10 items per sub-agent
2. **Explicit lists**: Give exact file paths, not patterns
3. **Verify counts**: Output item count = input count
4. **Isolated context**: Sub-agents don't know about other groups
5. **File-based communication**: Write to files, supervisor reads

---

## Grouping Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| By file | Each file is independent | 53 student blog posts |
| By topic | Files cluster by subject | Research papers by domain |
| By section | One large file with sections | Long report with chapters |
| By batch | Arbitrary even distribution | Any large uniform set |
