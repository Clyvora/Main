# Clyvora Technologies

[Clyvora](https://www.clyvora.tech/)—also known as Clyvora Tech or Clyvora Technologies—builds free, privacy-first browser tools. Selected files are processed on the user's device instead of being uploaded to a Clyvora processing server.

## Official projects

- [Clyvora Lens](https://www.lens.clyvora.tech/) inspects, searches, filters, and converts JSON and CSV files locally in the browser.
- [Clyvora Convert](https://www.convert.clyvora.tech/) converts local audio and video in the browser (**Beta**).
- [Clyvora Resize](https://www.resize.clyvora.tech/) resizes, compresses, and converts local images (**Beta**).
- [Clyvora Fetch](https://www.fetch.clyvora.tech/) retrieves available audio from supported public links when the user has permission (**Experimental**).

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
