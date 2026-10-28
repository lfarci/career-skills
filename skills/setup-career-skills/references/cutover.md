# Approved workspace cutover

Read **only when the user requests and authorizes** moving, archiving or replacing an existing workspace root. New setup and ordinary resumption do not require a cutover.

1. **Inventory.** List source files, mapped destinations, path collisions and references that would change. Scan links inside the old workspace **and inbound links from other accessible repository files**.
2. **Preserve evidence.** Summaries of source records are not a lossless migration. Keep the originals in an approved backup/archive or an equivalently accessible evidence store. Identify any new records that still link to the old paths.
3. **Plan and approve.** Show the intended moves, backup location and link rewrites before changing roots. Respect unrelated uncommitted work. Apply only the agreed cutover.
4. **Verify.** Check file preservation, links in the new root, links **into it** from elsewhere in the repository, and links inside the moved backup. Repair authorized broken references or report exceptions.
5. **Report coverage.** State checked paths, unresolved links and inaccessible parts. Claim a completed cutover only for the verified scope, and update the root checkpoint accordingly.

If source code, references or backing files cannot be inspected, record that limitation rather than claiming repository-wide link integrity. External publication remains separately authorized.
