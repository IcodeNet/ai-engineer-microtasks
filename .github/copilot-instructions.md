# AI Engineering Micro-Tasks - Copilot Instructions

## Repository Architecture

This is a **monorepo for micro-tasks** - each subdirectory contains an independent, self-contained task implementation:
- Pattern: `XX.micro-task-Y.Z-description/` (e.g., `01.micro-task-0.1-fastify-service/`)
- Each micro-task has its own `README.md`, source code, and may have its own dependencies
- Root `package.json` provides shared dependencies across micro-tasks

## Module System Configuration

**Critical**: This project uses ES modules (ESM) with CommonJS at the root:
- Root `package.json` has `"type": "commonjs"` for backward compatibility
- All micro-task code uses ES6 `import/export` syntax
- To run ES module code, tasks need their own `package.json` with `"type": "module"`

**Example**: `01.micro-task-0.1-fastify-service/` uses ESM imports but lacks task-level `package.json`:
```javascript
// server.js uses: import Fastify from 'fastify';
// routes/health.js uses: export default async function
```

**Fix pattern**: Add `package.json` to each micro-task directory:
```json
{
  "type": "module",
  "name": "@microtasks/task-name"
}
```

## Fastify Service Pattern (Micro-Task 0.1)

**Structure**: `src/server.js` → `src/routes/*.js` (individual route modules)
- Server: Fastify instance with logger enabled, listens on `0.0.0.0:3000`
- Routes: Exported as async plugin functions using `fastify.get()` registration
- **Missing**: `routes/index.js` aggregator (server.js tries to import non-existent file)

**Route registration pattern**:
```javascript
// Each route file exports a Fastify plugin
export default async function routeName(fastify, opts) {
  fastify.get('/endpoint', async (request, reply) => {
    return { data };
  });
}
```

**To add routes**: Create `routes/index.js` that registers all route plugins:
```javascript
import health from './health.js';
import info from './info.js';

export default async function routes(fastify, opts) {
  await fastify.register(health);
  await fastify.register(info);
}
```

## Running Micro-Tasks

**From root directory**:
```bash
# If task has proper package.json with "type": "module"
node 01.micro-task-0.1-fastify-service/src/server.js

# Or navigate to task directory
cd 01.micro-task-0.1-fastify-service
node src/server.js
```

**Current blocker**: ES module errors indicate missing task-level configuration.

## Development Workflow

1. **New micro-task**: Create numbered directory following pattern `XX.micro-task-Y.Z-name/`
2. **Task setup**: Add task-specific `package.json` if using ES modules
3. **Dependencies**: Install at root level for shared packages, or task-level for isolated needs
4. **Testing**: Currently no test framework configured (`npm test` exits with error)

## Key Files to Check

- `package.json` (root): Dependency versions, module type
- `01.micro-task-0.1-fastify-service/src/server.js`: Entry point, missing routes index
- `01.micro-task-0.1-fastify-service/src/routes/`: Individual route implementations

## Common Issues

- **"Cannot use import statement"**: Add `"type": "module"` to task's `package.json`
- **"Cannot find module './routes/index.js'"**: Create aggregator file or fix import path
- **Port conflicts**: Fastify server hardcoded to port 3000
