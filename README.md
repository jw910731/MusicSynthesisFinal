# Music Synthesis Final
Music synthesis course final project

# Setup
## Setup Python Guide
This project uses rye to manage python envirnoment and package dependency. More about how to install and use rye, see the following link: [https://rye-up.com/](https://rye-up.com/).

To get started, run the following command:
```bash
rye sync
source .venv/bin/activate
```

Add package as dependency by:
```bash
rye add <package>
```

Sync the dependency after installing new dependency:
```bash
rye sync
```
## Setup Web
This project include frontend code which need to install dependency by using pnpm

Get started by using the following command in **web** folder:
```bash
pnpm install
```

Build the website by using:
```bash
pnpm build
```
