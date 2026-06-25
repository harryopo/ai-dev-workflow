/**
 * Shared Todo domain types and storage interface.
 * Platform-agnostic business contracts used by Web, Mobile and Desktop adapters.
 */

export interface TodoItem {
  id: string
  name: string
  completed: boolean
}

export interface TodoStats {
  total: number
  completed: number
  pending: number
}

export interface TodoStorage {
  getItems(): Promise<TodoItem[]>
  addItem(name: string): Promise<TodoItem>
  updateItem(id: string, updates: Partial<Omit<TodoItem, 'id'>>): Promise<void>
  deleteItem(id: string): Promise<void>
}

export interface TodoServiceOptions {
  storage: TodoStorage
}
