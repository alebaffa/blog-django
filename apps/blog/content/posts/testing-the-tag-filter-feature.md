---
title: Testing the Tag Filter Feature
slug: testing-the-tag-filter-feature
status: published
published_at: 2026-03-14
tags:
  - dev
---

## Tags are now filterable!

This is a test post to verify the new tag filter menu on the homepage works correctly.

When you visit the homepage, you should now see a row of tag chips at the top of the post list. Clicking **#dev** will bring you to this dedicated tag page at `/tags/dev/`.

### What was built

- A `/tags/<slug>/` URL that shows only posts with that tag
- A pill-shaped chip menu above the post list
- The active tag is highlighted in the accent colour
- Pagination links stay within the tag context

Happy filtering!
