import type { TodoItem, TodoStats, TodoStorage } from './types'

/**
 * Pure business logic for Todo management.
 * Contains no UI or framework code and can be unit tested independently.
 */
export class TodoService {
  private storage: TodoStorage

  constructor(storage: TodoStorage) {
    this.storage = storage
  }

  async getItems(): Promise<TodoItem[]> {
    return this.storage.getItems()
  }

  async addItem(name: string): Promise<TodoItem> {
    const trimmed = name.trim()
    if (!trimmed) {
      throw new Error('项目名称不能为空')
    }
    return this.storage.addItem(trimmed)
  }

  async toggleItem(id: string): Promise<void> {
    const items = await this.storage.getItems()
    const item = items.find((i) => i.id === id)
    if (item) {
      await this.storage.updateItem(id, { completed: !item.completed })
    }
  }

  async deleteItem(id: string): Promise<void> {
    await this.storage.deleteItem(id)
  }

  getStats(items: TodoItem[]): TodoStats {
    const total = items.length
    const completed = items.filter((i) => i.completed).length
    return {
      total,
      completed,
      pending: total - completed,
    }
  }
}
