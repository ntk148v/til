# NextJS

## 1. Introduction

## 2. Project structure (nextjs15)

Source:

- <https://nextjs.org/docs/app/getting-started/project-structure>
- <https://www.wisp.blog/blog/the-ultimate-guide-to-organizing-your-nextjs-15-project-structure>

```text
├── src/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── utils/
│   └── styles/
├── public/
├── package.json
└── next.config.js
```

### 2.1. Core project structure

- One of the first decisions you'll face is whether to use a `src` directory. While Next.js works perfectly fine without it, using a `src` directory offers several benefits:
  - Clear separation between source code and configuration files
  - Easier to implement tooling and build processes
  - Cleaner root directory
  - More consistent with other JavaScript/TypeScript projects
- With Next.js 15's App Router, the `app` directory is where your routing magic happens. Here's how to structure it effectively:
  - Files directly in `app` affect the root route.
  - Folder create a new routes.
  - Parentheses `()` create route groups that don't affect the URL structure
  - Colocate non-routable files with folders `_folder`.
  - Parameterize segments with square brackets. Use `[segment]` for a single param, `[...segment]` for catch‑all, and `[[...segment]]` for optional catch‑all. Access values via the params prop.
  - Special files like `layout.tsx` and `page.tsx` serve specific purposes in the routing system

```text
src/app/
├── layout.tsx
├── page.tsx
├── (auth)/
│   ├── login/
│   └── register/
├── dashboard/
│   ├── layout.tsx
│   ├── page.tsx
│   └── settings/
└── api/
```

### 2.2. Organizing components

The components directory is often the heart of your Next.js application. Here's a proven structure that scales well:

```text
src/components/
├── ui/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   ├── Card/
│   └── Modal/
├── layout/
│   ├── Header/
│   ├── Footer/
│   └── Sidebar/
└── features/
    ├── auth/
    └── dashboard/
```

- The `ui` folder contains your basic building blocks - eusable components that aren't tied to specific business logic. These are your buttons, inputs, cards, and modals.
- Layout components are larger pieces that form your application's structure. They're typically used across multiple pages but might have more specific functionality than UI components.
- Feature components are tied to specific business features or domains. For example, a `LoginForm` component would go in `features/auth/`, while a `DashboardStats` component belongs in `features/dashboard/`.

### 2.3. Managing utilities and libraries

```text
src/
├── utils/
│   ├── formatting.ts
│   ├── validation.ts
│   └── helpers.ts
└── lib/
    ├── auth.ts
    ├── api.ts
    └── database.ts
```

- The `utils` directory should contain pure utility functions that:
  - Have no side effects
  - Don't depend on external services
  - Can be easily tested in isolation
- Examples include:
  - Date formatting functions
  - String manipulation helpers
  - Calculation utilities
- The `lib` directory is for more complex functionality that often:
  - Interfaces with external services
  - Contains business logic
  - Manages state or side effects
- Common examples include:
  - API client configurations
  - Authentication helpers
  - Database connections

### 2.4. State management and models

When using state management solutions like Zustand, organize your store files logically:

```text
src/
├── store/
│   ├── auth.store.ts
│   ├── user.store.ts
│   └── theme.store.ts
└── models/
    ├── user.model.ts
    └── product.model.ts
```

- Store organization: each store file should:
  - Focus on a specific domain
  - Export a single store instance
  - Include related actions and selectors
- The `models` directory contains TypeScript interfaces and type definitions that are used across your application:

```ts
// user.model.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: "user" | "admin";
}
```

### 2.5. Styling organization

```text
src/
├── styles/
│   ├── global.css
│   ├── variables.css
│   └── themes/
│       ├── light.css
│       └── dark.css
└── components/
    └── Button/
        ├── Button.tsx
        └── Button.module.css
```

- Keep global styles, variables, and theme definitions in the `styles` directory.
- For component-specific styles:
  - Use CSS Modules alongside component files.
  - Name them matching the component (e.g., Button.module.css for Button.tsx).
  - Keep them in the same folder as the component.
