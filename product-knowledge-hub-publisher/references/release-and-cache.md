# Release And Cache Checklist

## GitHub

1. Confirm `gh auth status` has the intended active account.
2. Confirm remote, default branch, worktree branch, and intended diff.
3. Run build and static checks before commit and again in CI.
4. Push a feature branch and create a PR. Merge only when release authority is explicit.

## Cloudflare Pages

1. Verify Pages project, production branch, build command, output directory, Node version, and custom-domain status.
2. Confirm the deployment associated with the merge commit succeeds.
3. Fetch the public domain and check for release-specific markup before calling the release live.

## Immutable Assets

`Cache-Control: immutable` is correct only when the asset URL changes for every content change.

Use content-hashed filenames when the build tool supports them. For a simple static generator, set a unique release version in every shared CSS/JS URL:

```html
<link rel="stylesheet" href="/assets/site.css?v={release-version}">
<script src="/assets/site.js?v={release-version}" defer></script>
```

Increment `{release-version}` for every asset change. Validate the public HTML contains the new URL, then inspect the live browser's computed styles rather than relying on a deployment status alone.
