## 📦 untrusted-python
> My blog post: [Running Untrusted Python](https://healeycodes.com/running-untrusted-python)

<br>

This is a sandbox for running untrusted Python code. Until it's been audited by someone with some kind of security authority, you should consider it to be insecure.

With that in mind, I welcome any bug reports, sandbox escapes, etc. – please raise an issue or email/DM me.

### Development

#### Fly.io backend

Install [flyctl](https://fly.io/docs/hands-on/install-flyctl/).

```bash
cd sandbox
fly launch
```

Follow the instructions in your terminal. Make a note of the URL – it will look like `https://foo.fly.dev`. Copy it (without a trailing slash!), and add it to `web/.env` as `API`.

#### Next.js frontend

```bash
npm i
npm run dev
```

Follow the instructions in your terminal.

### Deploy

`web` is a Next.js app that you can deploy to Vercel. Set the root directory of the project to `web`.

`sandbox` is a Fly.io app that has `fly.toml` file ready to use. Add the Fly.io URL as a Vercel environment variable as `API`.
