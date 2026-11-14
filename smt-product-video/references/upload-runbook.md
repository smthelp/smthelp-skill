# YouTube upload runbook — Smthelping channel

## Facts

- Channel: Smthelping — https://www.youtube.com/c/Smthelping
- Upload route: live browser → YouTube Studio. There is no API upload in this environment.
- The managed/server browser never shares the user's own device login. The upload always stops at the Google sign-in page and waits for the user.
- Idle browser sessions close after ~2 hours.
- Browser file grants have a size limit: ~115 MB passes, 185 MB failed. Use the compressed upload version, never the 200 MB+ master.

## Steps

1. **Confirm readiness with Jason first.** The upload session should be opened when he is ready to log in, not hours ahead.
2. Open a browser task at YouTube Studio (https://studio.youtube.com), stopped at the Google sign-in page. Tell Jason it is waiting.
3. Jason logs in to the Smthelping channel's Google account in that browser session and signals to continue. **Never ask for his password.**
4. In Studio: Create → Upload video → select the compressed upload version (`<PRODUCT>-4K-youtube.mp4`, ~100–120 MB). Wait for processing.
5. Fill in: title, description (paste from `youtube-description-final.txt`), thumbnail (upload the 1280×720 PNG), language English, category Science & Technology, visibility Public.
6. Upload the separate SRT as English captions.
7. Publish. Read back the published video page and record the URL.
8. Report the published URL to Jason. Replace the `[YouTube link]` placeholder in the social captions file with the real URL and re-deliver it.

## If the session expired

If the login session closed from idle timeout, reopen a fresh session stopped at the login page on Jason's say-so. The upload package (compressed file, thumbnail, SEO text) stays intact — nothing needs rebuilding.

## If upload is not possible now

Hand Jason the upload version + thumbnail + copy-paste SEO package for self-upload on a logged-in device. Record the status honestly as "upload not attempted" — never as published.

## After publication

- Verify the published page: title, description, thumbnail, captions all present.
- Update the social captions with the real YouTube URL.
- Record the published URL in the goal and in memory. Close the upload step only then.
