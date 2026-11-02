export type { TodoItem, TodoStats, TodoStorage, TodoServiceOptions } from './types'
export { TodoService } from './todoService'
export { useTodo, type UseTodoResult } from './hooks/useTodo'

// Platform-specific adapters are intentionally imported from their own files
// so that a project only pulls in the types and dependencies it actually uses:
//   import { WebStorageAdapter } from './storage/webStorage'
//   import { MobileStorageAdapter } from './storage/mobileStorage'
//   import { MemoryStorageAdapter } from './storage/memoryStorage'
