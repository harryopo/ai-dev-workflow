import type { TodoItem, TodoStorage } from '../types'

/**
 * In-memory TodoStorage implementation.
 * Useful for demos, tests, or platforms where persistent storage is not
 * available out of the box.
 */
export class MemoryStorageAdapter implements TodoStorage {
  private items: TodoItem[] = []

  async getItems(): Promise<TodoItem[]> {
    return [...this.items]
  }

  async addItem(name: string): Promise<TodoItem> {
    const item: TodoItem = {
      id: `${Date.now()}`,
      name,
      completed: false,
    }
    this.items.push(item)
    return item
  }

  async updateItem(id: string, updates: Partial<Omit<TodoItem, 'id'>>): Promise<void> {
    const index = this.items.findIndex((i) => i.id === id)
    if (index === -1) {
      return
    }
    this.items[index] = { ...this.items[index], ...updates }
  }

  async deleteItem(id: string): Promise<void> {
    this.items = this.items.filter((i) => i.id !== id)
  }
}
