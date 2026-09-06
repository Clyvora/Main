# Clyvora Technologies

[Clyvora](https://www.clyvora.tech/)—also known as Clyvora Tech or Clyvora Technologies—builds free, privacy-first browser tools. Selected files are processed on the user's device instead of being uploaded to a Clyvora processing server.

## Official projects

- [Clyvora Lens](https://www.lens.clyvora.tech/) inspects, searches, filters, and converts JSON and CSV files locally in the browser.
- [Clyvora Convert](https://www.convert.clyvora.tech/) converts local audio and video. Its next release combines image resizing, compression and conversion with explicit public SoundCloud retrieval and direct handoff into compatible local conversion.

Existing [Resize](https://www.resize.clyvora.tech/) and [Fetch](https://www.fetch.clyvora.tech/) links remain available during migration. This catalogue prepares the next release; it does not claim that the merger is deployed. Coordinate publication with Convert and ClyvoraAPI rollout. No redirects or domains were changed.

Only already publicly discoverable projects belong in this catalogue. A local repository or planned product alone does not establish permission to publish its identity or a URL.

The source for Clyvora projects is published through the [Clyvora GitHub organization](https://github.com/Clyvora).

Lens, Convert, and Resize process supported local files on-device. Fetch is networked: it sends the submitted public URL to ClyvoraAPI and the supported source platform. The deployed sites use Vercel Web Analytics for anonymous, cookie-free page-view statistics. No custom analytics events are configured, and selected filenames, file contents, and submitted URLs are not sent to analytics.

## Development

```bash
pnpm install
pnpm dev
```

Run `pnpm build` to type-check and create a production build.

## License

This website's original source code and content are proprietary. Copyright (c) 2026 Clyvora contributors. All rights reserved. See [LICENSE](LICENSE).
