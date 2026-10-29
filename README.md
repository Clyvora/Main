# Clyvora Technologies

[Clyvora](https://www.clyvora.tech/)—also known as Clyvora Tech or Clyvora Technologies—builds free, privacy-first browser tools. Selected files are processed on the user's device instead of being uploaded to a Clyvora processing server.

## Official projects

- [Clyvora Lens](https://www.lens.clyvora.tech/) inspects, searches, filters, and converts JSON and CSV files locally in the browser.
- [mewvi by Clyvora](https://mewvi.xyz/) downloads supported public media and converts local audio and video. Formerly Clyvora Convert; mewvi.xyz is its canonical address. Currently in beta, with provider-dependent download and collection support.
- [Live op Weg](https://liveopweg.nl/) shows live train locations on a map.

Existing [Resize](https://www.resize.clyvora.tech/) and [Fetch](https://www.fetch.clyvora.tech/) links remain available. The former Convert domains remain available during the move to mewvi; new catalogue links point to mewvi.xyz. Repository names and internal identifiers may retain `Convert` for compatibility.

Only already publicly discoverable projects belong in this catalogue. A local repository or planned product alone does not establish permission to publish its identity or a URL.

The source for Clyvora projects is published through the [Clyvora GitHub organization](https://github.com/Clyvora).

Lens, mewvi, and Resize process supported local files on-device. mewvi's public-link downloads contact Clyvora infrastructure and source platforms; its local conversion does not upload files. Fetch also sends submitted public URLs to ClyvoraAPI and supported source platforms. Live op Weg uses online railway data. This website uses Vercel Web Analytics for anonymous, cookie-free page-view statistics. No custom analytics events are configured, and selected filenames, file contents, and submitted URLs are not sent to analytics.

## Development

```bash
pnpm install
pnpm dev
```

Run `pnpm build` to type-check and create a production build.

## Homepage design

The homepage is a three-project gallery with local artwork, a monochrome Clyvora brand mark, and links to Lens, mewvi, and Live op Weg. mewvi keeps its own cat artwork; Clyvora keeps its original brand mark. The gallery responds to fine-pointer movement and uses Torph for text transitions; reduced-motion preferences disable movement. Both themes are supported, with dark as the default. The optional `clyvora-theme` localStorage value stores only the visitor's appearance preference. No remote font is required.

App artwork is stored in `public/apps/`. The interactive homepage requires JavaScript. The separate static About page provides project links and longer product and privacy information without requiring JavaScript.

## License

This website's original source code and content are proprietary. Copyright (c) 2026 Clyvora contributors. All rights reserved. See [LICENSE](LICENSE).
